import streamlit as st
from streamlit_option_menu import option_menu
from config import *
from About_Us import info
from Home import home
from Set_budget import budget
from Tracker import track
from Report import rep

st.set_page_config(layout=layout)

with st.sidebar:
    selected = option_menu(
            menu_title=None,  # required
            options=["About Us", "Home", "Set Budget", "Tracker", "Report"],
            icons=["info", "house", "calculator", "database", "bar-chart-fill"], 
            default_index=0,  # optional
            styles={
                "container": {"padding": "0!important", "background-color": "#FFFFFF"},
                "icon": {"color": "#42B781", "font-size": "18px"},
                "nav-link": {
                    "font-size": "18px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#A4D2C1",
                    "font-family": "Candara",
                },
                "nav-link-selected": {"background-color": "#519079"},
                },
            )

if selected == "About Us":
    info()

elif selected == "Home":
    home()

elif selected == "Set Budget":
    budget()

elif selected == "Tracker":
    track()

elif selected == "Report":
    rep()
