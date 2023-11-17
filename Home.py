import streamlit as st 
import pandas as pd
import os
from millify import millify
from config import *

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

try:
    df = pd.read_csv('data.csv', parse_dates=['Date'], dayfirst=True)
except (FileNotFoundError, pd.errors.EmptyDataError):
    df = pd.DataFrame(columns=['Type', 'Date', 'Category', 'Amount'])

display = st.columns([3, 1])
display[1].header("Mission")
display_r = display[0].columns(4)

if os.path.exists('data.csv'):
    total_income = df[df['Type'] == 'Income']['Amount'].sum()
    total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
    total_balance = total_income - total_expense
    total_saving = df[(df['Type'] == 'Income') & (df['Category'] == 'Saving')]['Amount'].sum()
else:
    total_income = 0
    total_expense = 0
    total_balance = 0
    total_saving = 0

with display_r[0]:
    total_balance_millified = millify(total_balance, precision=2)
    with st.container():
        st.subheader("Total Credits") 
        st.metric('Balance', f"{total_balance_millified} {currency}")

with display_r[1]:
    total_income_millified = millify(total_income, precision=2)
    with st.container():
        st.subheader("Total Income") 
        st.metric('Income', f"{total_income_millified} {currency}")

with display_r[2]:
    total_expense_millified = millify(total_expense, precision=2)
    with st.container():
        st.subheader("Total Expense") 
        st.metric('Expense', f"{total_expense_millified} {currency}")

with display_r[3]:
    total_saving_millified = millify(total_saving, precision=2)
    with st.container():
        st.subheader("Total Saving") 
        st.metric('Saving', f"{total_saving_millified} {currency}")
display[0].divider()