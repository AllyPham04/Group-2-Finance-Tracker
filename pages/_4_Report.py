import datetime as dt
import os
import pandas as pd
import plotly.express as px
import streamlit as st
import pytz
from config import *
from datetime import datetime

st.set_page_config(layout=layout)
st.title('Report')
# -----------------------------------------
ss = st.session_state
# side_bar = st.sidebar
try:
    file_path = 'data.csv'
    df = pd.read_csv(file_path, parse_dates=['Date'], dayfirst=True)
except (FileNotFoundError, pd.errors.EmptyDataError):
    df = pd.DataFrame(columns=['Type', 'Date', 'Category', 'Amount'])
# -----------------------------------------

now = datetime.now()
now_vn = now.astimezone(pytz.timezone('Asia/Ho_Chi_Minh'))

def summarize(summary_df):
# Set name which divided into 3 columns
    summary_income, summary_expense, summary_saving = st.columns(3)

    # Calculate each column
    summary_sum = summary_df.groupby(['Type'])['Amount'].sum()
    summary_sum_income = summary_sum.get('Income', 0)
    summary_sum_expense = summary_sum.get('Expense', 0)
    summary_sum_saving = summary_sum.get('Income', 0) - summary_sum.get('Expense', 0)

    # Write each column
    summary_income.subheader('Total Income')
    summary_income.subheader(f"{summary_sum_income:,}")
    summary_expense.subheader('Total Expense')
    summary_expense.subheader(f"{summary_sum_expense:,}")
    summary_saving.subheader('Balance')
    summary_saving.subheader(f"{summary_sum_saving:,}")


range_col_manual_select, range_col_quick_select = st.tabs(['Manual Selection', 'Quick Selection'])
with range_col_manual_select:

    with st.form('range_form', clear_on_submit=False):

        range_manual_start_date_input, range_manual_end_date_input = st.columns(2)
        range_manual_start_date_input = range_manual_start_date_input.date_input('From', value=now_vn.date(), format="DD/MM/YYYY")
        range_manual_end_date_input = range_manual_end_date_input.date_input('To', value=now_vn.date(), format="DD/MM/YYYY")
        range_manual_start_date = pd.to_datetime(
            range_manual_start_date_input, format='%Y-%m-%d')
        range_manual_end_date = pd.to_datetime(
            range_manual_end_date_input, format='%Y-%m-%d')

        range_df = df.copy()
        range_df['Date'] = pd.to_datetime(range_df['Date'])
        range_df = range_df[(range_df['Date'] >= range_manual_start_date) & (range_df['Date'] <= range_manual_end_date)]

        range_type = st.selectbox(label='Type', 
                                  options=['Income and Expense', 'Categories'])

        range_button = st.form_submit_button('Submit')
    options, summary = st.columns(2, gap='large')
    with options:
        if range_type == 'Income and Expense':
            visualize_type, tmp = st.columns(2)
            visual_df = range_df.groupby(['Date', 'Type'])['Amount'].sum()
            visual_df = visual_df.reset_index()
            visualize_type = visualize_type.selectbox('Visualization', ['Line chart', 'Bar chart'])
        elif range_type == 'Categories':
            visual_df = range_df
            # visual_df = visual_df.reset_index()
            # ---------------------------------------------------
            # De cai o visualization no ngan di
            with st.form('visualize_categories', clear_on_submit=False):
                visualize_type, visualize_cate_type = st.columns(2)
                visualize_type = visualize_type.selectbox('Visualization type', ['Line chart', 'Bar chart', 'Pie chart'])
                visualize_cate_type = visualize_cate_type.selectbox('Type', ['Income', 'Expense'])
                visualize_submit = st.form_submit_button('Submit')
    with summary:
        summarize(range_df)


    visualization = st.container()
    with visualization:
        if range_type == 'Income and Expense':
            if visualize_type == 'Line chart':

                visual = px.line(
                    visual_df,
                    x='Date',
                    y='Amount',
                    color='Type'
                )
                st.plotly_chart(visual, use_container_width=True)

            elif visualize_type == 'Bar chart':

                visual = px.bar(
                    visual_df,
                    x='Date',
                    y='Amount',
                    color='Type',
                    barmode="group",
                )
                st.plotly_chart(visual, use_container_width=True)

            # ------------------------------------------------------
        elif range_type == 'Categories':
            if visualize_cate_type == 'Income':
                income_df = visual_df[visual_df['Type'] == 'Income']
                income_df = income_df.groupby(['Category', 'Date'])['Amount'].sum().reset_index().sort_values(by='Date')

                if visualize_type == 'Line chart':

                    visual = px.line(
                        income_df,
                        x='Date',
                        y='Amount',
                        color='Category'
                    )
                    st.plotly_chart(visual, use_container_width=True)

                elif visualize_type == 'Bar chart':

                    visual = px.bar(
                        income_df,
                        x='Date',
                        y='Amount',
                        color='Category',
                        barmode="stack",
                    )
                    st.plotly_chart(visual, use_container_width=True)

                elif visualize_type == "Pie chart":

                    visual = px.pie(
                        income_df,
                        values='Amount',
                        names='Category'
                    )
                    st.plotly_chart(visual, use_container_width=True)

            elif visualize_cate_type == 'Expense':
                expense_df = visual_df[visual_df['Type'] == 'Expense']
                expense_df = expense_df.groupby(['Category', 'Date'])[
                    'Amount'].sum().reset_index().sort_values(by='Date')

                if visualize_type == 'Line chart':

                    visual = px.line(
                        expense_df,
                        x='Date',
                        y='Amount',
                        color='Category'
                    )
                    st.plotly_chart(visual, use_container_width=True)

                elif visualize_type == 'Bar chart':

                    visual = px.bar(
                        expense_df,
                        x='Date',
                        y='Amount',
                        color='Category',
                        barmode="stack",
                    )
                    st.plotly_chart(visual, use_container_width=True)

                elif visualize_type == "Pie chart":

                    visual = px.pie(
                        expense_df,
                        values='Amount',
                        names='Category'
                    )
                    st.plotly_chart(visual, use_container_width=True)

with range_col_quick_select:
    quick_select, tmp = st.columns([1,4])
    quick_select = quick_select.selectbox('By',['Week', 'Month', 'Year'])

    weekdays = ['Monday', 'Monday', 'Tuesday', 'Tuesday', 'Wednesday', 'Wednesday', 'Thursday',
                'Thursday', 'Friday', 'Friday', 'Saturday', 'Saturday', 'Sunday', 'Sunday']

    today = dt.date.today()

    range_quick_start_date = today - dt.timedelta(days=today.weekday())
    range_quick_end_date = today + dt.timedelta(days=6 - today.weekday())
    range_type, tmp = st.columns([1,4])
    range_type = range_type.selectbox(label='Type', options=['Income and Expense'])
    quick_sub_button, quick_add_button, quick_date_text, tmp = st.columns([.05, .05, .2, .6], gap='medium')

    if 'quick_change_var' not in ss:
        ss.quick_change_var = 0

    def quick_sub_def():
        ss.quick_change_var -= 1

    def quick_add_def():
        ss.quick_change_var += 1
    quick_sub_button = quick_sub_button.button(':arrow_backward:', key='range_sub_button', on_click=quick_sub_def)
    quick_add_button = quick_add_button.button(':arrow_forward:', key='range_add_button', on_click=quick_add_def)

    range_quick_start_date = range_quick_start_date + dt.timedelta(days=7 * ss.quick_change_var)
    range_quick_end_date = range_quick_end_date + dt.timedelta(days=7 * ss.quick_change_var)
    date_text = f'<div style="border: 2px solid #A0A0A0; font-size: 20px; text-align: center;"> From {range_quick_start_date} to {range_quick_end_date}</div>'
    quick_date_text = quick_date_text.markdown(date_text, unsafe_allow_html=True)

    range_quick_start_date = pd.to_datetime(range_quick_start_date, format='%d-%m-%Y')
    range_quick_end_date = pd.to_datetime(range_quick_end_date, format='%d-%m-%Y')

    range_quick_df = df.copy()
    range_quick_df['Date'] = pd.to_datetime(range_quick_df['Date'])
    range_condition = (range_quick_df['Date'] >= range_quick_start_date) & (range_quick_df['Date'] <= range_quick_end_date)
    range_quick_df = range_quick_df[range_condition]

    # Select chart
    options, summary = st.columns(2)
    with options:
        if range_type == 'Income and Expense':
            visual_df = range_quick_df.groupby(['Date', 'Type'])['Amount'].sum().reset_index()
            date_range = pd.date_range(start=range_quick_start_date, end=range_quick_end_date, freq='D')
            date_type_combinations = pd.MultiIndex.from_product([date_range, df['Type'].unique()], names=['Date', 'Type'])

            # Reindex the DataFrame with the date and type combinations
            visual_df = (
                visual_df.set_index(['Date', 'Type'])
                .reindex(date_type_combinations, fill_value=0)
                .reset_index()
            )
            visual_df = visual_df[(visual_df['Type'] != 0) | (visual_df['Amount'] != 0)]
            visualize_type, tmp = st.columns(2)
            visualize_type = visualize_type.selectbox('Charts', ['Line chart', 'Bar chart'])

    with summary:
        summarize(range_quick_df)

    visualization = st.container()
    with visualization:
        if range_type == 'Income and Expense':
            if visualize_type == 'Line chart':

                visual = px.line(
                    visual_df,
                    x=weekdays,
                    y='Amount',
                    color='Type'
                )
                st.plotly_chart(visual, use_container_width=True)
            #
            elif visualize_type == 'Bar chart':

                visual = px.bar(
                    visual_df,
                    x=weekdays,
                    y='Amount',
                    color='Type',
                    barmode="stack",
                )
                st.plotly_chart(visual, use_container_width=True)

             # ------------------------------------------------------
rank_income, rank_expense, tmp = st.columns([1,1,2])

with rank_income:
    st.header('Top Income')
    rank_income_df = df.copy()
    rank_income_df = rank_income_df.groupby('Category')['Amount'].sum()
    # rank_income_df = rank_income_df.sort_values('Amount', ascending=False)
    st.dataframe(rank_income_df)

with rank_expense:
    st.header('Top Expense')
    rank_expense_df = df.copy()
    rank_expense_df = rank_expense_df.groupby('Category')['Amount'].sum()
    # rank_expense_df = rank_expense_df.sort_values('Amount', ascending=False)
    st.dataframe(rank_expense_df)
