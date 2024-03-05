import streamlit as st
import pandas as pd
import os
import components.common as common
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
    if os.getenv('snowflake_env') == 'local':
        print('is not Snowflake')

        # setup appropriate arguments depending on the options provided
        ckwargs = {
            'user':os.getenv('snowflake_user')
            ,'account':os.getenv('snowflake_account') 
            ,'role':os.getenv('snowflake_role')
            ,'warehouse':os.getenv('snowflake_warehouse')            
            ,'database':os.getenv('snowflake_database')
            ,'schema':os.getenv('snowflake_schema')
            }
        
        # add authenticator if setup to use SSO or use specified password
        if os.getenv('snowflake_authenticator') == 'externalbrowser':
            ckwargs['authenticator'] = os.getenv('snowflake_authenticator')
        else:
            ckwargs['password'] = os.getenv('snowflake_pwd')
        
        # setup snowflake connector
        conn = snowflake.connector.connect(**ckwargs)
        
        # set the session object
        result = Session.builder.configs({"connection": conn}).create()
    else:
        print('is Snowflake')

        # use existing active if not running in a Native App or Snowflake env.
        result = get_active_session()
    
    return result

@st.cache_data(show_spinner=False)
def get_dataFromQuery(query) -> pd.DataFrame:
    #run the supplied query and keep on streamlit cache as a resource
    #retrieve with snowflake session and return as pandas
    try:
        query_main_df = get_snow_session().sql(query)
        pandas_main_df = query_main_df.to_pandas()
        return pandas_main_df
    except Exception as err:

        common.display_error(f'Error occurred while trying to query the database.',err)

def get_metricActiveConfig() -> str:
    #provided the base query to read the metrics that are defined in the data
    return f"""
        select
        b.metric_id
        ,b.subject
        ,b.name 
        ,b.metric_type
        ,b.label
        ,b.help_text
        ,b.trend_normal
        ,b.output_format
        ,b.data_function1
        ,b.data_function2
        from item_poc.history.metric_all_active b
        ;
        """

@st.cache_data(show_spinner=False)
def get_formatTranslation(value=None):
    snowflake_dict = {
            'Decimal 0': ',.0f'
            ,'Decimal 2': ',.2f'
            ,'Percentage 0': ',.0%'
            ,'Percentage 2': ',.2%'
            }
    if value is not None:
        result = snowflake_dict.get(value)
    else:
        result = snowflake_dict

    return result

def get_metricTypes():
    result = ['sum','rate']
    return result

def get_metricSubjects():
    result = ['query','task']
    return result
