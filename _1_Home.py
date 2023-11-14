import streamlit as st 
from config import *

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ""
user_name = st.text_input("Enter your name:")
st.session_state['user_name'] = user_name
st.header(f"Welcome, {user_name}!")