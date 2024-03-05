import streamlit as st
import os
import PIL.Image as image
import numpy as np
import plotly.express as px
import pandas as pd
import components.data as data

def display_image() -> None:
    # display the image from the setup folder using plotly
    # see https://medium.com/evolv-consulting/evolving-streamlit-in-snowflake-f9a319fb95f7
    
    if os.getenv('snowflake_env') == 'local':
        img_loc = './setup\data_evolved_logo.png'
    else:
        img_loc = 'data_evolved_logo.png'

    im = np.asarray(image.open(img_loc))
    fig = px.imshow(im)
    fig.update_traces(hovertemplate=None,hoverinfo='skip')
    fig.update_layout(width=300,height=200,margin=dict(l=0, r=0, b=0, t=0))
    fig.update_xaxes(showticklabels=False,showgrid=False,zeroline=False)
    fig.update_yaxes(showticklabels=False,showgrid=False,zeroline=False)
    st.plotly_chart(fig,config={'displayModeBar': False})

def display_header(pageHeader:str,showSlider:bool=False) -> None:
    #displays the header of the page including the logo and sets the page config settings
    st.set_page_config(layout='wide', page_title=pageHeader)

    #keep the slider from going across the entire page
    #add image to right side 
    headerCols = st.columns([3,2,1,1])

    with headerCols[0]:
        
        #create 2 CRs to center the header and slider with the logo
        for i in range(2):
            st.write('\n')

        st.header(pageHeader)

        if showSlider:
            #get selection of history limits to review to drive dataframe output later
            st.slider(label=f'Select the number of historical days to review.'
                ,key='choose_historyDays'
                ,min_value=1
                ,max_value=90
                ,value=76
                ,help=f'Use this to adjust the number of historical days to represent in the metrics below.'
                )

    with headerCols[3]:
        display_image()

    st.divider()

def rate(part, whole) -> float:
    #function for taking the rate of two numbers 
    #accepts ints and floats for numerator (part) and denominator (whole)
    if whole == 0:
        result = 0.0
    else:
        result = float(part) / float(whole) 
    return float(result)

def get_metricdeltacolor(value,showNormal=True) -> str:
    #determines if the trend line of the metric should display normally or not or if the value is 0 then turn off
    if value == '0.00%':
        return 'off'
    else:
        if showNormal:
            return 'normal'
        else:
            return 'inverse'
        
def display_metric(metric_df:pd.DataFrame) -> st.metric:
    #takes the metric config information pulled from the db and the corresponding results of the query already aggregated to current value and prior value
    #then creates a streamlit metric object and passes back for display    

    delta = format(rate((metric_df.iloc[0]['CURRENT_VALUE'] - metric_df.iloc[0]['PRIOR_VALUE']),metric_df.iloc[0]['CURRENT_VALUE']),f',.2%')
    delta_color = get_metricdeltacolor(delta,str2bool(metric_df.iloc[0]['TREND_NORMAL']))

    result = st.metric(
        label=metric_df.iloc[0]['LABEL'],
        value=format(metric_df.iloc[0]['CURRENT_VALUE'], f'{data.get_formatTranslation(metric_df.iloc[0]["OUTPUT_FORMAT"])}'),
        delta=delta,
        delta_color=delta_color,
        help=metric_df.iloc[0]['HELP_TEXT'],
        label_visibility="visible"
        )
    return result

def refresh_page() -> None:
    #forces a rerun of the page using functions appropriate for the current or previous versions of streamlit
    if st.__version__ >= '1.27.0':
        st.rerun()
    else:
        st.experimental_rerun()

def reset_CacheOnClick() -> None:
    #forces a reset of the streamlit data and resource cache
    st.cache_resource.clear()
    st.cache_data.clear()

def check_for_zero(kpi_df, metric, aggregateType='value') -> int:
    #function for aggregating kpis from dataframe 
    #expects dataframe, loc metric and aggregate type 
    #returns result defaults to 0 if null'''
    if kpi_df.shape[0] > 0:
        if aggregateType == 'value':
            result = int(kpi_df.iloc[0][metric])
        elif aggregateType == 'sum':    
            result = int(sum(kpi_df.loc[:,(metric)]))
        elif aggregateType == 'unique':
            result = int(len(pd.unique(kpi_df.loc[:,(metric)])))            
    else:
        result = int(0)
    return result

def get_current_metric_filtered(df:pd.DataFrame) -> pd.DataFrame:
    if df.shape[0] > 0:
        results = df[df.loc[:,('HISTORICAL_DAYS')] <= st.session_state.choose_historyDays].copy()
    else:
        results = None
    
    return results

def get_prior_metric_filtered(df:pd.DataFrame) -> pd.DataFrame:
    if df.shape[0] > 0:
        results = df[(df.loc[:,('HISTORICAL_DAYS')] > st.session_state.choose_historyDays) & (df.loc[:,('HISTORICAL_DAYS')] <= (st.session_state.choose_historyDays * 2))].copy()
    else:
        results = None
    
    return results

def str2bool(checkValue:str) -> bool:
    # since boolean conversion using bool() basically checks for existence of any value and always returns True if any value exists
    # this will check a specific list of true/false values and set explicitly
    if str(checkValue).lower() in ('true','t','yes','y','1','positive','+','on'):
        results = True
    elif str(checkValue).lower() in ('false','f','no','n','0','negative','-','off'):
        results = False
    else:
        display_error(f'Error occurred in converting string to boolean for the value "{checkValue}"','Invalid Value.')
    return results

def display_error(errorMessage:str,errorException:str):
    st.error(f'''{errorMessage}:  {str(errorException)}''',icon='🚨')

def get_aggregates(index:int,metric_type:str,*df:pd.DataFrame) -> pd.DataFrame:
    '''aggregate to the Current and Prior Values for the metric using the number of days from the slider
    use metric type to determine if: 
        sum=single value current and prior - expect 1 dfs to be passed [0] = values,
        rate=numerator and denominator values calculated into a rate or average current and prior - expect 2 dfs to be passed [0] = numerator, [1] = denominator
    
    Current range = 1 - slider number
    Prior range = slider+1 - slider*2 
    '''

    try:
        if metric_type == 'sum':

            current_value = check_for_zero(get_current_metric_filtered(df[0]), 'VALUE', aggregateType='sum')
            prior_value = check_for_zero(get_prior_metric_filtered(df[0]), 'VALUE', aggregateType='sum')
        
        if metric_type == 'rate':

            if df[1] is not None:

                n_current_value = check_for_zero(get_current_metric_filtered(df[0]), 'VALUE', aggregateType='sum')
                n_prior_value = check_for_zero(get_prior_metric_filtered(df[0]), 'VALUE', aggregateType='sum')

                d_current_value = check_for_zero(get_current_metric_filtered(df[1]), 'VALUE', aggregateType='sum')
                d_prior_value = check_for_zero(get_prior_metric_filtered(df[1]), 'VALUE', aggregateType='sum')

                current_value = rate(n_current_value,d_current_value)
                prior_value = rate(n_prior_value,d_prior_value)

            else:
                raise Exception('Invalid configuration: Rate metric expects both a numerator and a denominator result.')

        results =  pd.DataFrame({'METRIC_ID':[index],'CURRENT_VALUE':[current_value],'PRIOR_VALUE':[prior_value]},index=[index])   

        return results
    
    except Exception as err:
        display_error(f'An error occurred while trying to combine aggregates METRIC_ID {index}',err)

