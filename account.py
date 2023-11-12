import streamlit as st
from config import *

def app():
    user_name = st.text_input(f'Name:', "Enter your name")
    st.header(f"Welcome, {user_name}!")
    total_balance = 0
    total_income = 0
    total_expense = 0

    col1, col2, col3 = st.columns(3)
    
    col1.metric("Total Income", f"{total_income} {currency}")
    col2.metric("Total Expense", f"{total_expense} {currency}")
    col3.metric("Total Balance", f"{total_balance} {currency}")


    st.header("**Transaction**")
    
    for transaction in transactions:
        st.write(f'{transaction["Category"]} ({transaction["Date"]})')
        amount = transaction["Amount"]
        if transaction["Type"] == "Income":
            st.write(f'+ {amount} {currency}')
        else:
            st.write(f'- {amount} {currency}')