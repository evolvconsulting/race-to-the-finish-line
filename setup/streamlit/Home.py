
import streamlit as st
import components.common as common


common.display_header(pageHeader='Home')

#setup some constant values for Colums to display
#initialize session state variables
st.session_state['display_columns'] = 6

st.write('Imagine that each time a user came up with a new measurement to report on, they had to wait days or even weeks for an SDLC to run the requirement through its paces before being able to see the metric in their dashboard.  This project introduces a simple but effective solution improving speed to market with your application by introducing a data-driven approach and framework to adding metrics to your dashboard.')

st.write('Click the button below to reset the cached data to force re-query from the database.')
if st.button('Refresh Cache Data',type='primary'):
    st.cache_data.clear()
    st.cache_resource.clear()
    common.refresh_page()
