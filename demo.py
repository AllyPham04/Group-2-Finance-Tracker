#import plotly.express as px
import streamlit as st 
#from streamlit_option_menu import option_menu 
#import csv
from config import *
from menu import get_selected_option
from account import app as account_app
from set_budget import app as set_budget_app
from tracker import app as tracker_app
from report import app as report_app

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)


# --- MENU ---
selected = get_selected_option()
#-------------

if selected == "Account":
    account_app()

if selected == "Set Budget":
    set_budget_app()

if selected == "Tracker":
    tracker_app()

if selected == "Report":
    report_app()