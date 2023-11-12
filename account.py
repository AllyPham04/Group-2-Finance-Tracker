import streamlit as st
from config import *
from tracker import *

def app():
    if 'user_name' not in st.session_state:
        st.session_state['user_name'] = ' '

    st.session_state['user_name'] = st.text_input("**Enter your name:**", st.session_state.get('user_name', ''))
    st.header(f"Welcome, {st.session_state['user_name']}!")


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


    st.header("**Transaction**")
    
    if os.path.exists('data.csv'):
        df = pd.read_csv('data.csv')
    else:
        df = pd.DataFrame()

    if not df.empty:
        df = df.sort_values(by='Date', ascending=False)
        for date, transactions in df.groupby(df["Date"]):
            st.subheader(date)
            for _, transaction in transactions.iterrows():
                amount = transaction["Amount"]
                if transaction["Type"] == "Income":
                    st.write(f'- {transaction["Category"]}: \+ {amount} {currency}')
                elif transaction["Type"] == "Expense":
                    st.write(f'- {transaction["Category"]}: \- {amount} {currency}')
    
    if st.button("Clear all data"):
        st.session_state.clear()
        if os.path.exists('data.csv'):
            os.remove('data.csv')
            st.success("Data cleared!")
        col1.empty()
        col2.empty()
        col3.empty()