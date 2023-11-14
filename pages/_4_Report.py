import streamlit as st
from config import *
import plotly.express as px

st.header("Report")
with st.form("saved_periods"):
    period = st.selectbox("Select period:", ["2022_March"])
    submitted = st.form_submit_button("Plot period")
    if submitted:
        comment = "Some comment"
        incomes = {"Salary": 1500, "Blog": 50, "Other Income": 10}
        expenses = {"Rent": 600, "Utilities": 200, "Groceries": 300, "Car": 100,
                    "Other Expenses": 50,"Saving": 10}

        total_income = sum(incomes.values())
        total_expense = sum(expenses.values())
        remaining_budget = total_income - total_expense

        col6, col7, col8 = st.columns(3)

        col6.metric("Total Income", f"{total_income} {currency}")
        col7.metric("Total Expense", f"{total_expense} {currency}")
        col8.metric("Remaining Budget", f"{remaining_budget} {currency}")

        col9, col10 = st.columns(2)
            
        fig_incomes = px.pie(values=list(incomes.values()), names=list(incomes.keys()), title="Income Chart")
        col9.plotly_chart(fig_incomes, use_container_width=True)

        fig_expenses = px.pie(values=list(expenses.values()), names=list(expenses.keys()), title='Expense Chart')
        col10.plotly_chart(fig_expenses, use_container_width=True)

        st.text(f"Comment: {comment}")