from config import *
import streamlit as st
import pandas as pd
import os

def budget():
    local_css('style.css')
    background()
    st.title("Set Budget")

    #Divide screen into 2 columns
    col1, col2 = st.columns(2)

    #Get list of expenses and set budget for each category
    with col1:
        st.subheader("Set Budget")
        for category in expenses:
            with st.form(key=f"{category}_expense_form"):
                colb_1, colb_2, colb_3 = st.columns([3, 1, 1], gap="medium")

                #Nhập vào budget
                budget = colb_1.number_input(f"{category} Budget:", min_value=0, format="%i", step=10)
                colb_2.write(" ")
                colb_2.write(" ")
                colb_3.write(" ")
                colb_3.write(" ")

                #Thêm nút Add
                if colb_2.form_submit_button("Add"):
                    try:
                        budget_df = pd.read_csv('budget.csv')
                    except (FileNotFoundError, pd.errors.EmptyDataError):
                        budget_df = pd.DataFrame(columns=['Type', 'Category', 'Budget'])

                    #Nếu đã nhập budget cho category A trước đấy thì khi nhập lại sẽ hiện cảnh báo
                    if not ((budget_df['Type'] == 'Expense') & (budget_df['Category'] == category)).any():
                        budget_data = {'Type': 'Expense', 'Category': category, 'Budget': budget}
                        budget_df = pd.concat([pd.DataFrame([budget_data]), budget_df], ignore_index=True)
                        budget_df.to_csv('budget.csv', index=False)
                        st.success("Data saved!")
                    else:
                        st.warning("Data for this category already exists")
                        st.warning("Please update the data instead")

                #Update budget cho category đã nhập
                if colb_3.form_submit_button("Update"):
                    try:
                        budget_df = pd.read_csv('budget.csv')
                        budget_df.loc[(budget_df['Type'] == 'Expense') & (budget_df['Category'] == category), 'Budget'] = budget
                        budget_df.to_csv('budget.csv', index=False)
                        st.success("Data updated!")
                    except (FileNotFoundError, pd.errors.EmptyDataError):
                        st.warning("No budget data found")

    #Hiện Budget cho từng category
    with col2:
        with st.container():
            st.subheader("Budget Data")
            try:
                budget_df = pd.read_csv('budget.csv')
                budget_df.index = budget_df.index + 1
                st.dataframe(budget_df[budget_df['Type'] == 'Expense'], use_container_width=True)
            except (FileNotFoundError, pd.errors.EmptyDataError):
                budget_df = pd.DataFrame(columns=['Type', 'Category', 'Budget'])
                st.warning("No budget data found")

            clear_data = st.button("Clear All Data")

            if clear_data:
                if os.path.exists("budget.csv"):
                    os.remove("budget.csv")
                    st.success("All data cleared!")
