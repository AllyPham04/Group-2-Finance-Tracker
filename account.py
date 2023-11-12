import streamlit as st
from config import *
from tracker import *

if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ''

def app():
    st.session_state['user_name'] = st.text_input(f'Name:', st.session_state['user_name'])
    st.header(f"Welcome, {st.session_state['user_name']}!")
    total_balance = 0
    total_income = 0
    total_expense = 0

    col1, col2, col3 = st.columns(3)
    
    col1.metric("Total Income", f"{total_income} {currency}")
    col2.metric("Total Expense", f"{total_expense} {currency}")
    col3.metric("Total Balance", f"{total_balance} {currency}")


    st.header("**Transaction**")
    
    df = pd.read_csv('data.csv')

    df = df.sort_values(by='Date', ascending=False)

    for _, transaction in df.iterrows():
        st.write(f'{transaction["Category"]} ({transaction["Date"]})')
        amount = transaction["Amount"]
        if transaction["Type"] == "Income":
            st.write(f'* +{amount} {currency}')
        elif transaction["Type"] == "Expense":
            st.write(f'* -{amount} {currency}')