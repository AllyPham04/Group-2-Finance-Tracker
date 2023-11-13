import streamlit as st

def get_selected_option():
    return st.sidebar.radio(label="Menu", 
                                options=["Account", "Set Budget", "Tracker", "Report"])