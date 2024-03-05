
import streamlit as st
import components.common as common


common.display_header(pageHeader='Home')

#setup some constant values for Colums to display
#initialize session state variables
#default to 4
if 'display_columns' not in st.session_state:
    st.session_state['display_columns'] = 4

cols = st.selectbox('How many columns do you want to display?',index=(st.session_state['display_columns']-1),options=(1,2,3,4,5,6,7,8))
if cols is not None:
    st.session_state['display_columns'] = cols 

st.write('Imagine that each time a user came up with a new measurement to report on, they had to wait days or even weeks for an SDLC to run the requirement through its paces before being able to see the metric in their dashboard.  This project introduces a simple but effective solution improving speed to market with your application by introducing a data-driven approach and framework to adding metrics to your dashboard.')

st.write('Click the button below to reset the cached data to force re-query from the database.')
if st.button('Refresh Cache Data',type='primary'):
    st.cache_data.clear()
    st.cache_resource.clear()
    common.refresh_page()
