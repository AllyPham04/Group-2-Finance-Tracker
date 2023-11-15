import streamlit as st
import os
import pandas as pd
import plotly.express as px
from config import *
from datetime import datetime
from millify import millify

st.title("Tracker")
col_a1, col_a2, col_a3 = st.columns([0.2, 0.4, 0.4])
#st.divider()
col_b1, col_b2 = st.columns(2)
now = datetime.now()

total_income = 0
total_expense = 0

if 'previous_total_balance' not in st.session_state:
    st.session_state['previous_total_balance'] = 0

previous_total_balance = st.session_state['previous_total_balance']

with col_b1:
    tab1, tab2 = st.tabs(["Income", "Expense"])
        
    with tab1:
        with st.form("income", clear_on_submit=True):
            st.subheader("Transaction")
            selected_date = st.date_input("Select date:", value=datetime.today(), format="DD/MM/YYYY")
            amount = st.number_input(f"Amount:", min_value=0, format="%i", step=10)
            category = st.selectbox("Category:", incomes)
            if st.form_submit_button("Save Data"):
                # Gather user inputs
                user_data = {
                    'Type': 'Income',
                    'Date': selected_date.strftime("%d-%m-%Y"),
                    'Category': category,
                    'Amount': amount
                }
                                
                try:
                    history_df = pd.read_csv('data.csv')
                    #budget_df = pd.read_csv('budget.csv')
                except (FileNotFoundError, pd.errors.EmptyDataError):
                    history_df = pd.DataFrame(columns=user_data.keys())
                    #budget_df = pd.DataFrame(columns=['Type', 'Category', 'Budget'])
                                
                history_df = pd.concat([pd.DataFrame(user_data, index=[0]), history_df], ignore_index=True)
                history_df['Date'] = pd.to_datetime(history_df['Date'], format="%d-%m-%Y")
                history_df = history_df.sort_values(by=['Date'], ascending=False)
                history_df.to_csv('data.csv', index=False, date_format="%d-%m-%Y")

                st.success("Data saved!")                

    with tab2:
        with st.form("expense", clear_on_submit=True):
            st.subheader("Transaction")
            selected_date = st.date_input("Select date:", value=datetime.today(), format="DD/MM/YYYY")
            amount = st.number_input(f"Amount:", min_value=0, format="%i", step=10)
            category = st.selectbox("Category:", expenses)
            if st.form_submit_button("Save Data"):
                # Gather user inputs
                user_data = {
                    'Type': 'Expense',
                    'Date': selected_date.strftime("%d-%m-%Y"),
                    'Category': category,
                    'Amount': amount
                }
                                
                try:
                    history_df = pd.read_csv('data.csv')
                except (FileNotFoundError, pd.errors.EmptyDataError):
                    history_df = pd.DataFrame(columns=user_data.keys())
                            
                history_df = pd.concat([pd.DataFrame(user_data, index=[0]), history_df], ignore_index=True)
                history_df['Date'] = pd.to_datetime(history_df['Date'], format="%d-%m-%Y")
                history_df = history_df.sort_values(by=['Date'], ascending=False)
                history_df.to_csv('data.csv', index=False, date_format="%d-%m-%Y")

                st.success("Data saved!")

with col_b2:
    with st.form("transactions_history", clear_on_submit=True):
        st.subheader("History")
        if os.path.exists('data.csv'):
            history_df = pd.read_csv('data.csv', parse_dates=True, dayfirst=True)
            total_income = history_df[history_df['Type'] == 'Income']['Amount'].sum()
            total_expense = history_df[history_df['Type'] == 'Expense']['Amount'].sum()
            total_balance = total_income - total_expense
            total_saving = history_df[(history_df['Type'] == 'Income') & (history_df['Category'] == 'Saving')]['Amount'].sum()
        else:
            history_df = pd.DataFrame()
            total_balance = 0
            total_saving = 0

        if os.path.exists('budget.csv') and os.path.exists('data.csv'):
            budget_df = pd.read_csv('budget.csv')
            for expense in expenses:
                budget_expense = budget_df[budget_df['Category'] == category]['Budget'].values[0]
                expense_cate = history_df[(history_df['Type'] == 'Expense') & (history_df['Category'] == expense)]['Amount'].sum()
                if (expense_cate > 0.9 * budget_expense).any():
                    st.warning(f"You have spent over 90% of your budget for {expense} category")
        else:
            pass

        if not history_df.empty:
            history_df.index = history_df.index + 1
            history_df['Amount'] = history_df.apply(lambda row: f'+ {row["Amount"]} {currency}' 
                                    if row['Type'] == 'Income' 
                                    else f'- {row["Amount"]} {currency}', axis=1)
            #history_df['Month'] = history_df['Date'].dt.strftime("%m")
            history_container = st.dataframe(history_df.drop(columns='Type'), use_container_width=True)
        
        if st.form_submit_button("Clear all data"):
            st.session_state.clear()
            if os.path.exists('data.csv'):
                os.remove('data.csv')
                st.success("Data cleared!")
            user_income.clear()
            user_expense.clear()
st.session_state['previous_total_balance'] = total_balance

delta_balance = total_balance - previous_total_balance
delta_balance_millified = millify(delta_balance, precision=2)

with col_a1:
    total_balance_millified = millify(total_balance, precision=2)
    with st.container():
        st.subheader("Total Credits") 
        st.metric('Balance', f"{total_balance_millified} {currency}", delta=f"{delta_balance_millified} {currency}", delta_color="normal")
    
with col_a2:
    col_a2_1, col_a2_2 = st.columns(2)
    col_a2_1.subheader("Saving Goal")

    saving_goal = col_a2_1.number_input("Enter your saving goal:", min_value=0, format="%i", step=10)

    progress = total_saving / saving_goal if saving_goal > 0 else 0

    if col_a2_1.button("Save"):
        col_a2_1.write(f'Your saving goal is {saving_goal} {currency}')
        if total_saving >= saving_goal:
            st.success("Congratulations! You have reached your saving goal!")
        elif total_saving == 0:
            st.warning("You have not saved anything yet!")
        else:
            fig_saving = px.pie(values=[total_saving, saving_goal - total_saving], 
                            names=["Saving", "Remaning"], 
                            title=f'Saving Progress')
            col_a2_2.plotly_chart(fig_saving, use_container_width=True)

with col_a3:
    pass
    #code ở đây