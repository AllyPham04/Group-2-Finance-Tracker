import streamlit as st

from config import *

st.set_page_config(layout="centered")
st.markdown("<h1 style='text-align: center;'>Finance Tracker</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    .reportview-container {
        background: ("money_falling.gif") no-repeat center center fixed; 
        -webkit-background-size: cover;
        -moz-background-size: cover;
        -o-background-size: cover;
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)