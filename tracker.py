import streamlit as st
from config import *
import pandas as pd

def app():
    st.header(f"Income")
    with st.form("income_form", clear_on_submit=True):
        selected_date = st.date_input("Select date:", format="DD/MM/YYYY")
        category = st.selectbox("Category:", incomes)
        amount = st.number_input(f"Amount:", min_value=0, format="%i", step=10)
        submitted = st.form_submit_button("Save Data")
        if submitted:
            period = selected_date.strftime("%d-%m-%Y")
            # Gather user inputs
            user_data = {'Type': 'Income', 'Date': period, 'Category': category, 'Amount': amount}
            
            try:
                df = pd.read_csv('data.csv')
            except FileNotFoundError:
                df = pd.DataFrame(columns=user_data.keys())
            
            df = pd.concat([df, pd.DataFrame(user_data, index=[0])], ignore_index=True)
            df.to_csv('data.csv', index=False)
            
            user_income.append({"Category:": category, "Amount": amount})
            st.write(f"Category: {category}: {amount} {currency}")
            st.success("Data saved!")
            transactions.append(user_data)
    

    st.header(f"Expense")
    with st.form("expense_form", clear_on_submit=True):
        selected_date = st.date_input("Select date:", format="DD/MM/YYYY")
        category = st.selectbox("Category:", expenses)
        amount = st.number_input(f"Amount:", min_value=0, format="%i", step=10)
        submitted = st.form_submit_button("Save Data")
        if submitted:
            period = selected_date.strftime("%d-%m-%Y")
            # Gather user inputs
            user_data = {'Type': 'Expense','Date': period, 'Category': category, 'Amount': amount}
            
            try:
                df = pd.read_csv('data.csv')
            except FileNotFoundError:
                df = pd.DataFrame(columns=user_data.keys())
            
            df = pd.concat([df, pd.DataFrame(user_data, index=[0])], ignore_index=True)
            df.to_csv('data.csv', index=False)
            
            user_expense.append({"Category:": category, "Amount": amount})
            st.write(f"Category: {category}: {amount} {currency}")
            st.success("Data saved!")
            transactions.append(user_data)