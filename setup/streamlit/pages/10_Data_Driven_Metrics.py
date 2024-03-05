
import logging
import threading
import time
import datetime
import pandas as pd
import concurrent.futures
import components.data as data
import components.common as common
import streamlit as st
import streamlit.runtime.scriptrunner as script 

common.display_header(pageHeader='Data-Driven Metrics',showSlider=True)

def prepare_metric_data(index:int,metric_type:str,ctx:script.ScriptRunContext,*query:pd.DataFrame):
    #get the results of the query specified and return the results- called from the thread pool executor to distribute asynchronously

    #add script context to allow streamlit to properly leverage worker threads
    script.add_script_run_ctx(threading.current_thread(),ctx)

    df1 = None
    df2 = None

    try:
        if query[0] is not None:
            df1 = data.get_dataFromQuery(query[0])
            #add the index into the results for later use
            df1['METRIC_ID'] = index

        if query[1] is not None:
            df2 = data.get_dataFromQuery(query[1])
            #add the index into the results for later use
            df2['METRIC_ID'] = index        
        
        #get aggregate values for each of the potential 2 dfs
        #the agg function will return a single df
        results = common.get_aggregates(index,metric_type,df1,df2)

    except Exception as err:
        common.display_error(f'An error occurred while trying to prepare METRIC_ID {index}',err)

    return results

def run_multiThreads():
    metric_df = data.get_dataFromQuery(data.get_metricActiveConfig())

    if metric_df.shape[0] > 0:

        item_count = metric_df.shape[0]

        if item_count > 0:
            segments = item_count
            initial = 5
            step_value = int((100 / (segments + 1)))

            prgBar = st.progress(initial, text='Retrieving Metrics...')
            
            cols = st.columns(st.session_state['display_columns'])
            conts = st.container()

            with concurrent.futures.ThreadPoolExecutor(max_workers=item_count) as executor:
                #get script context for the main thread to pass to the worker threads and add context for those threads
                ctx = script.get_script_run_ctx()
                
                #initiate all of the threads
                results = [executor.submit(prepare_metric_data
                                        , metric_df.iloc[i]['METRIC_ID']
                                        , metric_df.iloc[i]['METRIC_TYPE']
                                        , ctx
                                        , metric_df.iloc[i]['DATA_FUNCTION1']
                                        , metric_df.iloc[i]['DATA_FUNCTION2']) 
                                        for i in range(item_count)]

                i = 0
                for future in concurrent.futures.as_completed(results):
                    #dynamically distribute results amongst a specified number of columns
                    progress = initial + (step_value * (i+1))                    
                    prgBar.progress(progress)
                    
                    try:

                        result_df = future.result()
                
                        with cols[i % st.session_state['display_columns']]:
                            #join the 2 dataframes to ensure the config matches the resulting values
                            combined_df = pd.merge(metric_df,result_df,how='inner',on=['METRIC_ID'])
                            common.display_metric(combined_df)

                            i += 1

                    except Exception as err:
                        common.display_error(f'An error occurred while trying to process METRIC_ID {metric_df.iloc[i]["METRIC_ID"]}',err)

                prgBar.progress(100, text='Refresh Complete.')
                time.sleep(0.1)
                prgBar.empty()    
    else:
        st.warning(f'No metrics available for the options selected.')        

start = datetime.datetime.now()
run_multiThreads()
end = datetime.datetime.now()
# st.write(f'Total Processing time = {end - start}.')

