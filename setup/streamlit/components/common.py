import streamlit as st
import os
import PIL.Image as image
import numpy as np
import plotly.express as px

# display the image from the setup folder using plotly
# see https://medium.com/evolv-consulting/evolving-streamlit-in-snowflake-f9a319fb95f7

def display_image() -> None:
    if os.getenv('emoji_env') == 'local':
        img_loc = './setup\data_evolved_logo.png'
    else:
        img_loc = 'data_evolved_logo.png'

    im = np.asarray(image.open(img_loc))
    fig = px.imshow(im)
    fig.update_traces(hovertemplate = None,hoverinfo = "skip")
    fig.update_layout(width=300,height=200,margin=dict(l=0, r=0, b=0, t=0))
    fig.update_xaxes(showticklabels=False,showgrid=False,zeroline=False)
    fig.update_yaxes(showticklabels=False,showgrid=False,zeroline=False)
    st.plotly_chart(fig,config={'displayModeBar': False})

def display_header(pageHeader:str,showDivider:bool=True) -> None:
    #keep the slider from going across the entire page
    #add image to right side 
    headerCols = st.columns([3,2,1,1])

    with headerCols[0]:
        for i in range(2):
            st.write('\n')

        st.header(pageHeader)

        #get selection of history limits to review to drive dataframe output later
        st.slider(label=f'Select the number of historical executions to review.'
            ,key='choose_historyLimit'
            ,min_value=1
            ,max_value=20
            ,value=10
            ,help=f"Use this to adjust the number of historical executions to represent in the visuals below."
            )

    with headerCols[3]:
        display_image()

    st.divider()