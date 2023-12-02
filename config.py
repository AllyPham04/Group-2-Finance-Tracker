import streamlit as st
import base64

incomes = ["Salary", "Saving", "Bonus", "Interest", "Side Job", "Tax refund", "Other"]
expenses = ["Food", "Household", "Clothes", "Subscription", "Health", "Entertainment", "Education", "Utilities", "Transportation", "Investment", "Other"]
currency = "VND"
page_title = "Personal Finance Tracker"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "wide"
fontFamily = 'Candara'
app_name = 'KEEPEE'

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
        return base64.b64encode(data).decode()

def local_css(file_name):#func to read css file -> create flake
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def background_about_us():
    bg_img = get_img_as_base64("bg_1.png")
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("data:image/png;base64,{bg_img}");
    background-size: 100%;
    background-repeat: no-repeat;
    background-attachment: local;
    }}
    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)

def background():
    bg_img = get_img_as_base64("bg_2.png")
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("data:image/png;base64,{bg_img}");
    background-size: 100%;
    background-repeat: no-repeat;
    background-attachment: local;
    }}
    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)
