from config import *
import streamlit as st
import pandas as pd
import os

st.title("Set Budget ")

col1, col2 = st.columns([5, 5])
with col1:
    st.subheader("Set Budget")
    for category in expenses:
        with st.form(key=f"{category}_expense_form"):
            colb_1, colb_2, colb_3 = st.columns([3, 1, 1], gap="medium")
            budget = colb_1.number_input(f"{category} Budget:", min_value=0, format="%i", step=10)
            colb_2.write(" ")
            colb_2.write(" ")
            colb_3.write(" ")
            colb_3.write(" ")
            if colb_2.form_submit_button("Add"):
                try:
                    budget_df = pd.read_csv('budget.csv')
                except (FileNotFoundError, pd.errors.EmptyDataError):
                    budget_df = pd.DataFrame(columns=['Type', 'Category', 'Budget'])

                if not ((budget_df['Type'] == 'Expense') & (budget_df['Category'] == category)).any():
                    budget_data = {'Type': 'Expense', 'Category': category, 'Budget': budget}
                    budget_df = pd.concat([pd.DataFrame([budget_data]), budget_df], ignore_index=True)
                    budget_df.to_csv('budget.csv', index=False)
                    st.success("Data saved!")
                else:
                    st.warning("Data for this category already exists")
                    st.warning("Please update the data instead")

            if colb_3.form_submit_button("Update"):
                try:
                    budget_df = pd.read_csv('budget.csv')
                    budget_df.loc[(budget_df['Type'] == 'Expense') & (budget_df['Category'] == category), 'Budget'] = budget
                    budget_df.to_csv('budget.csv', index=False)
                    st.success("Data updated!")
                except (FileNotFoundError, pd.errors.EmptyDataError):
                    st.warning("No budget data found")

with col2:
    with st.form("budget", clear_on_submit=True):
        st.subheader("Budget Data")
        try:
            budget_df = pd.read_csv('budget.csv')
            budget_df.index = budget_df.index + 1
            st.markdown("Expense Budget")
            st.dataframe(budget_df[budget_df['Type'] == 'Expense'])
        except (FileNotFoundError, pd.errors.EmptyDataError):
            budget_df = pd.DataFrame(columns=['Type', 'Category', 'Budget'])
            st.warning("No budget data found")
        if st.form_submit_button("Clear all data"):
            st.session_state.clear()
            if os.path.exists('budget.csv'):
                os.remove('budget.csv')
                st.success("Data cleared!")