import streamlit as st
import os
import pandas as pd
from config import *
from datetime import datetime

def app():
    col_a1, col_a2 = st.columns(2)
    now = datetime.now()

    total_balance = 0
    total_income = 0
    total_expense = 0

    for income in user_income:
        total_income += income["Amount"]
    for expense in user_expense:
        total_expense += expense["Amount"]
    total_balance = total_income - total_expense
    with col_a1:
        with st.form("add_transaction", clear_on_submit=True):
            st.subheader("Transaction")
            type = st.radio("Type:",
                            ["Income", "Expense"])
            st.date_input("Select date:", value=datetime.today(), format="DD/MM/YYYY")
            amount = st.number_input(f"Amount:", min_value=0, format="%i", step=10, key="amount_input")
            if type == "Income":
                category = st.selectbox("Category:", incomes)
                if st.form_submit_button("Save Data"):
                    # Gather user inputs
                    user_data = {
                        'Type': 'Income',
                        'Date': now.strftime("%H:%M:%S %d-%m-%Y"),
                        'Category': category,
                        'Amount': amount
                    }
                        
                    try:
                        df = pd.read_csv('data.csv')
                    except (FileNotFoundError, pd.errors.EmptyDataError):
                        df = pd.DataFrame(columns=user_data.keys())
                        
                    df = pd.concat([df, pd.DataFrame(user_data, index=[0])], ignore_index=True)
                    df = df.sort_values(by=['Date'], ascending=False)
                    df.to_csv('data.csv', index=False, date_format='%d-%m-%Y %H:%M:%S')

                    st.write(f"{category}: {amount} {currency}")
                    st.success("Data saved!")
                    user_income.append({"Category:": category, "Amount": amount})
            if type == "Expense":
                category = st.selectbox("Category:", expenses)
                if st.form_submit_button("Save Data"):
                    # Gather user inputs
                    user_data = {
                        'Type': 'Expense',
                        'Date': now.strftime("%H:%M:%S %d-%m-%Y"),
                        'Category': category,
                        'Amount': amount
                    }
                        
                    try:
                        df = pd.read_csv('data.csv')
                    except (FileNotFoundError, pd.errors.EmptyDataError):
                        df = pd.DataFrame(columns=user_data.keys())
                        
                    df = pd.concat([df, pd.DataFrame(user_data, index=[0])], ignore_index=True)
                    df = df.sort_values(by=['Date'], ascending=False)
                    df.to_csv('data.csv', index=False, date_format='%d-%m-%Y %H:%M:%S')

                    st.write(f"{category}: {amount} {currency}")
                    st.success("Data saved!")
                    user_expense.append({"Category:": category, "Amount": amount})

    with col_a2:
        with st.form("transactions_history", clear_on_submit=True):
            st.subheader("History")
            if os.path.exists('data.csv'):
                df = pd.read_csv('data.csv')
            else:
                df = pd.DataFrame()

            if not df.empty:
                df.index = df.index + 1
                df['Amount'] = df.apply(lambda row: f'+ {row["Amount"]} {currency}' if row['Type'] == 'Income' else f'- {row["Amount"]} {currency}', axis=1)
                st.table(df.drop(columns=['Type']))

            if st.form_submit_button("Clear all data"):
                st.session_state.clear()
                if os.path.exists('data.csv'):
                    os.remove('data.csv')
                    st.success("Data cleared!")
                user_income.clear()
                user_expense.clear()