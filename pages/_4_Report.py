import os
import pandas as pd
import plotly.express as px
import streamlit as st
import pytz
from config import *
from datetime import datetime

# -----------------------------------------
st.set_page_config(layout=layout)
st.title('Report')
# side_bar = st.sidebar
try:
    df = pd.read_csv('data.csv', parse_dates=['Date'], dayfirst=True)
except (FileNotFoundError, pd.errors.EmptyDataError):
    df = pd.DataFrame(columns=['Type', 'Date', 'Category', 'Amount'])
# -----------------------------------------

range_col, summary_col = st.columns([1, 2], gap='medium')
# range_col.title("COL 1")
# summary_col.title("COL 2")

now = datetime.now()
now_vn = now.astimezone(pytz.timezone('Asia/Ho_Chi_Minh'))

with range_col:
    # range_col_manual_select, range_col_quick_select = st.tabs(['Manual Selection', 'Quick Selection'])
    #
    # with range_col_manual_select:
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
    # with range_col_quick_select:
    #     quick_select = st.selectbox('By',['Week', 'Month', 'Year'])
    #     weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    #     today = dt.date.today()
    #     range_quick_start_date = today - dt.timedelta(days=today.weekday())
    #     range_quick_end_date = today + dt.timedelta(days=6 - today.weekday())
    #
    #     minus_var = st.session_state.get('minus_var', 0)
    #     test_minus_button = st.button('Click here to go to previous week')
    #     if test_minus_button:
    #         minus_var += 1
    #         st.session_state['minus_var'] = minus_var
    #
    #
    #     range_quick_start_date = range_quick_start_date - dt.timedelta(days=7 * minus_var)
    #     range_quick_end_date = range_quick_end_date - dt.timedelta(days=7 * minus_var)
    #     st.write(range_quick_start_date, range_quick_end_date)

with summary_col:
    # Set name which divided into 3 columns
    summary_income, summary_expense, summary_saving = st.columns(3)

    # Calculate each column
    summary_sum = range_df.groupby(['Type'])['Amount'].sum()
    summary_sum_income = summary_sum.get('Income', 0)
    summary_sum_expense = summary_sum.get('Expense', 0)
    summary_sum_saving = summary_sum.get('Income', 0) - summary_sum.get('Expense', 0)

    # Write each column
    summary_income.subheader('Total Income')
    summary_income.metric('Income', f"{summary_sum_income} {currency}")
    summary_expense.subheader('Total Expense')
    summary_expense.metric('Expense', f"{summary_sum_expense} {currency}")
    summary_saving.subheader('Total Balance')
    summary_saving.metric('Balance', f"{summary_sum_saving} {currency}")

if not df.empty:
    visualize_type, temp = st.columns([1, 8])
    if range_type == 'Income and Expense':
        visual_df = df.groupby(['Date', 'Type'])['Amount'].sum()
        visual_df = visual_df.reset_index()
        visualize_type = visualize_type.selectbox('Visualization', 
                                                ['Line chart', 'Bar chart'])
    elif range_type == 'Categories':
        visual_df = range_df
        # visual_df = visual_df.reset_index()
        # ---------------------------------------------------
        # De cai o visualization no ngan di
        visualize_opt, tmp = st.columns([1, 3])

        with visualize_opt:
            with st.form('visualize_categories', clear_on_submit=False):
                visualize_type, visualize_cate_type = st.columns(2)
                visualize_type = visualize_type.selectbox('Visualization type', 
                                                        ['Line chart', 'Bar chart', 'Pie chart'])
                visualize_cate_type = visualize_cate_type.selectbox('Type', 
                                                                    ['Income', 'Expense'])
                visualize_submit = st.form_submit_button('Submit')

    visualization, ranking_income, ranking_expense = st.columns([2, 1, 1], gap='medium')
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

    with ranking_income:
        ranking_income.header('Income')
        rank_income_df = df[df['Type'] == 'Income'].copy()
        rank_income_df = rank_income_df.groupby(['Category'])['Amount'].sum()
        st.dataframe(rank_income_df.head(5), use_container_width=True)

    with ranking_expense:
        ranking_expense.header('Expense')
        rank_expense_df = df[df['Type'] == 'Expense'].copy()
        rank_expense_df = rank_expense_df.groupby(['Category'])['Amount'].sum()
        st.dataframe(rank_expense_df.head(5), use_container_width=True)
