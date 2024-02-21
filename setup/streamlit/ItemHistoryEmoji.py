import streamlit as st
import pandas as pd
import components.data as data
import components.common as common
import tabulate

st.set_page_config(layout="wide", page_title='Historical Presentation')

common.display_header(pageHeader='Using a Data-Driven Emoji Column')

# output the display dataframes
displayCols = st.columns([2,1,3])

with displayCols[0]:
    #select which option to output  Pattern or Stoplight
    st.selectbox('What type of emoji do you want to use for Item History?'
        ,key='choose_emojiGroup'
        ,options=['Pattern','Stoplight','Weather', 'Smiley Face','Moon Phase']
        ,index=None
        ,help=f'Use this to select the type of emojis to use for Item History output.'
        )

with displayCols[2]:
    if st.session_state['choose_emojiGroup'] is not None:

        #retrieve the data for the success history line
        emoji_df = data.get_dataFromQuery(
            data.get_emojiHistory(
                st.session_state['choose_emojiGroup']
                ,st.session_state['choose_historyLimit']
                )
            ).set_index('ITEM_NAME')

        st.subheader(f'Emoji History Column')
        #setup the presentation using the emoji content column to show the successes, failures, or incompletes over history
        st.markdown(emoji_df.to_markdown())
