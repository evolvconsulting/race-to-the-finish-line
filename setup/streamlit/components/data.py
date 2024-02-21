import streamlit as st
import pandas as pd
import os
import snowflake.connector
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
import dotenv as env 

# load environment variables if exists
env.load_dotenv('./setup\settings.env')  # take environment variables from .env.

def get_snow_session() -> Session:
    
    # if no local env variable exists, assume running from Native App and leverage existing active session
    # else use local env variables to connect:
    # Create the following env variables for your environment in a settings.env file in the setup folder of the project once downloaded
    if os.getenv('emoji_env') == 'local':
        print('is not Snowflake')

        # setup snowflake connector
        conn = snowflake.connector.connect(
                authenticator=(os.getenv('emoji_snowflake_authenticator')) # use for SSO connection
                ,user=(os.getenv('emoji_snowflake_user'))
                ,password=(os.getenv('emoji_snowflake_pwd')) 
                ,account=(os.getenv('emoji_snowflake_account')) 
                ,role=(os.getenv('emoji_snowflake_role'))
                ,warehouse=(os.getenv('emoji_snowflake_warehouse'))              
                ,database=(os.getenv('emoji_snowflake_database'))
                ,schema=(os.getenv('emoji_snowflake_schema')) 
                )
        
        # set the session object
        result = Session.builder.configs({"connection": conn}).create()
    else:
        print('is Snowflake')

        # use existing active if not running in a Native App or Snowflake env.
        result = get_active_session()
    
    return result

def get_dataFromQuery(query) -> pd.DataFrame:
    query_main_df = get_snow_session().sql(query)
    pandas_main_df = query_main_df.to_pandas()
    return pandas_main_df

def get_progressHistory(historyLimit:int) -> str:
    return f'''
        with last_items as (
            select 
            ih.item_name
            ,ih.execution_status
            from item_poc.history.item_history ih
            qualify (row_number() over(partition by item_name order by ih.execution_timestamp desc)) <= {historyLimit}
        )
        select 
        lt.item_name
        ,sum(case when execution_status = 'Successful' then 1 else 0 end) / {historyLimit} as results
        from last_items lt
        group by lt.item_name
        order by lt.item_name
        ;
        '''

def get_lineHistory(historyLimit:int) -> str:
    return f'''
        with last_items as (
            select 
            ih.item_name
            ,ih.execution_status
            from item_poc.history.item_history ih
            qualify (row_number() over(partition by item_name order by ih.execution_timestamp desc)) <= {historyLimit}
        )
        select 
        lt.item_name
        ,listagg(case when execution_status = 'Successful' then 1 else 0 end,', ') as results
        from last_items lt
        group by lt.item_name
        order by lt.item_name
        ;
        '''

def get_emojiHistory(emojiGroup:str,historyLimit:int) -> str:
    return f'''
        with last_items as (
            select 
            ih.item_name
            ,ih.execution_status
            from item_poc.history.item_history ih
            qualify (row_number() over(partition by item_name order by ih.execution_timestamp desc)) <= {historyLimit}
        )
        select 
        lt.item_name
        ,listagg(es.emoji_content) as results
        from last_items lt 
        join item_poc.history.execution_status es
            on lt.execution_status = es.execution_status
            and es.emoji_group = '{emojiGroup}'
        group by lt.item_name
        order by lt.item_name
        ;
        '''
