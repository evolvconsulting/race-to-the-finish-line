import streamlit as st
import pandas as pd
import components.data as data
import components.common as common

st.set_page_config(layout="wide", page_title='Historical Presentation')

common.display_header(pageHeader='Using a Plotly Scatter Chart')

#retrieve the data for the bar graph option
graph_df = data.get_dataFromQuery(data.get_graphHistory(st.session_state["choose_historyLimit"]))

st.subheader(f'Plotly Scatter Chart')

#setup the presentation using the plotly scatter to show the status over history
fig_graph = common.prepare_px_figure(graph_df
                                    ,xaxis='EXECUTION_DATE'
                                    ,xlabel='Date'
                                    ,yaxis='ITEM_NAME'
                                    ,ylabel='Item'
                                    ,color='EXECUTION_STATUS'
                                    ,colorlabel='Status'
                                    )
st.plotly_chart(fig_graph, theme='streamlit', use_container_width=True)