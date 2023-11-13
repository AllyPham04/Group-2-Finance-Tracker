import streamlit as st
from config import *
from tracker import *

def app():
    total_balance = 0
    total_income = 0
    total_expense = 0

    for income in user_income:
        total_income += income["Amount"]
    for expense in user_expense:
        total_expense += expense["Amount"]
    total_balance = total_income - total_expense

    col1, col2, col3 = st.columns(3)
    
    col1.metric("Total Income", f"{total_income} {currency}")
    col2.metric("Total Expense", f"{total_expense} {currency}")
    col3.metric("Total Balance", f"{total_balance} {currency}")