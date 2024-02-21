import streamlit as st
import pandas as pd
import components.data as data
import components.common as common

st.set_page_config(layout="wide", page_title='Historical Presentation')

common.display_header(pageHeader='Using a Data_Editor Configuration Column')

#retrieve the data for the success rate
progress_df = data.get_dataFromQuery(data.get_progressHistory(st.session_state["choose_historyLimit"]))

#retrieve the data for the success history line
line_df = data.get_dataFromQuery(data.get_lineHistory(st.session_state["choose_historyLimit"]))

#display all together but with a small gap between them.
displayCols = st.columns([3,1,3,1,3])

with displayCols[0]:
    st.subheader(f'Progress Column')

    #setup the presentation using the progress column to show the percentage of success over history
    st.data_editor(
        progress_df
        ,column_config={
            'ITEM_NAME': st.column_config.TextColumn(
                label=f'Item Name'
                ,help=f'The name of the Item that was executed.'
                ,width=None
                )
            ,'RESULTS': st.column_config.ProgressColumn(
                label=f'Success Rate (last {st.session_state["choose_historyLimit"]} executions)'
                ,help=f'The number of sucessful executions within the last {st.session_state["choose_historyLimit"]} executions for each Item.'
                ,width=None
                #format='%f' #default to percentage
                ,min_value=0
                ,max_value=1
                )}
        ,hide_index=True
        ,use_container_width=True
    )

with displayCols[2]:
    st.subheader(f'Line Chart Column')

    #setup the presentation using the line chart column to show the success over history
    st.data_editor(
        line_df
        ,column_config={
            'ITEM_NAME': st.column_config.TextColumn(
                label=f'Item Name'
                ,help=f'The name of the Item that was executed.'
                ,width=None
                )
            ,"RESULTS": st.column_config.LineChartColumn(
                label=f'Item Success History (last {st.session_state["choose_historyLimit"]} executions)'
                ,help=f'The status of executions within the last {st.session_state["choose_historyLimit"]} executions for each Item.'
                ,width=None
                ,y_min=0
                ,y_max=1
            )}
        ,hide_index=True
        ,use_container_width=True
    )

with displayCols[4]:
    st.subheader(f'Bar Chart Column')

    #setup the presentation using the bar chart column to show the success over history
    #since its the same as the line, will just reuse the line output
    st.data_editor(
        line_df
        ,column_config={
            'ITEM_NAME': st.column_config.TextColumn(
                label=f'Item Name'
                ,help=f'The name of the Item that was executed.'
                ,width=None
                )
            ,"RESULTS": st.column_config.BarChartColumn(
                label=f'Item Success History (last {st.session_state["choose_historyLimit"]} executions)'
                ,help=f'The status of executions within the last {st.session_state["choose_historyLimit"]} executions for each Item.'
                ,width=None
                ,y_min=0
                ,y_max=1
            )}
        ,hide_index=True
        ,use_container_width=True
    )