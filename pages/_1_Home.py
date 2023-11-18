import streamlit as st 
import pandas as pd
import os
import matplotlib.pyplot as plt
import plotly.express as px
from millify import millify
from datetime import timedelta
from datetime import datetime
from config import *

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

try:
    df = pd.read_csv('data.csv', parse_dates=['Date'], dayfirst=True)
    df['Date'] = pd.to_datetime(df['Date'], format="%d-%m-%Y")
    df['Date'] = df['Date'].dt.date
except (FileNotFoundError, pd.errors.EmptyDataError):
    df = pd.DataFrame(columns=['Type', 'Date', 'Category', 'Amount'])

display = st.columns([3, 1])
display[1].header("Mission")
display_r1 = display[0].columns(4)

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

with display_r1[0]:
    total_balance_millified = millify(total_balance, precision=2)
    with st.container():
        st.subheader("Total Credits") 
        st.metric('Balance', f"{total_balance_millified} {currency}")

with display_r1[1]:
    total_income_millified = millify(total_income, precision=2)
    with st.container():
        st.subheader("Total Income") 
        st.metric('Income', f"{total_income_millified} {currency}")

with display_r1[2]:
    total_expense_millified = millify(total_expense, precision=2)
    with st.container():
        st.subheader("Total Expense") 
        st.metric('Expense', f"{total_expense_millified} {currency}")

with display_r1[3]:
    total_saving_millified = millify(total_saving, precision=2)
    with st.container():
        st.subheader("Total Saving") 
        st.metric('Saving', f"{total_saving_millified} {currency}")

button_left = display_r1[0].button("Next Week")
button_right = display_r1[1].button("Last Week")
current_date = datetime.now()

if 'start_date' not in st.session_state:
    st.session_state['start_date'] = current_date - timedelta(days=(current_date.weekday() - 0) % 7)
    st.session_state['start_date'] = st.session_state['start_date'].date()

if 'weekly_data' not in st.session_state:
    st.session_state['weekly_data'] = pd.DataFrame()
    weekly_data = st.session_state['weekly_data']
displayr2 = display[0].columns([2, 1])
with displayr2[0]:
    with st.container():
        st.subheader("Weekly Chart")
        
        if button_left:
            st.session_state['start_date'] += timedelta(weeks=1)
        
        if button_right:
            st.session_state['start_date'] -= timedelta(weeks=1)

        date_range = pd.date_range(start=st.session_state['start_date'], periods=7)
        weekly_data = df[(df['Date'] >= st.session_state['start_date']) & (df['Date'] < st.session_state['start_date'] + timedelta(weeks=1))]
        
        all_days_data = pd.DataFrame({'Date': date_range})
        all_days_data['Date'] = pd.to_datetime(all_days_data['Date']).dt.date

        df_resampled = weekly_data.groupby(['Date', 'Type'])['Amount'].sum()
        df_resampled = df_resampled.reset_index()
        df_resampled['Type'] = pd.Categorical(df_resampled['Type'], categories=['Income', 'Expense'], ordered=True)
            
        all_days_data = pd.MultiIndex.from_product([all_days_data['Date'], ['Income', 'Expense']], names=['Date', 'Type']).to_frame(index=False)
        
        df_resampled = pd.merge(all_days_data, df_resampled, on=['Date', 'Type'], how='left', sort=True)

        df_resampled['Amount'].fillna(0, inplace=True)

        visual_bar = px.bar(df_resampled, x="Date", y="Amount", color="Type", barmode="group")
        st.plotly_chart(visual_bar, use_container_width=True)

with displayr2[1]:
    with st.container():
        st.subheader("All Expenses")

        date_range = pd.date_range(start=st.session_state['start_date'], periods=6)
        
        weekly_expenses = weekly_data[weekly_data['Type'] == 'Expense']
        
        #all_days_data = pd.DataFrame({'Date': date_range})
        if not weekly_expenses.empty:
            expenses_by_category = weekly_expenses.groupby('Category')['Amount'].sum().reset_index()

            visual_pie = px.pie(expenses_by_category, values='Amount', names='Category', hole=0.5)
            st.plotly_chart(visual_pie, use_container_width=True)
        else:
            st.warning("No expense data available for the selected week.")