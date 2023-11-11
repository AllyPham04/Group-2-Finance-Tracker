import plotly.express as px
import streamlit as st 
from streamlit_option_menu import option_menu 
import csv

#---------------------------------------
incomes = ["Salary", "Pocket Money", "Bonus", "Side Job", "Investment", "Other Income"]
expenses = ["Food", "Clothes", "Houseware", "Cosmetic", "Exchange", "Education", "Electric Bill", "Transportation", "Other Expense"]
currency = "VND"
page_title = "Personal Finance Tracker"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)


# --- MENU ---
selected = option_menu(menu_title=None, 
                       options=["Set Budget", "Tracker", "Visualization"], 
                       icons=["coin", "database-fill", "bar-chart"], 
                       orientation="horizontal")
#-------------

if selected == "Set Budget":
    pass

if selected == "Tracker":
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
            
            with open('data.csv', 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=user_data.keys())
                
                # If the file is empty, write the header
                if csvfile.tell() == 0:
                    writer.writeheader()

                # Write the user's data
                writer.writerow(user_data)
                
            st.success("Data saved!")
    
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
            
            with open('data.csv', 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=user_data.keys())
                
                # If the file is empty, write the header
                if csvfile.tell() == 0:
                    writer.writeheader()

                # Write the user's data
                writer.writerow(user_data)
                
            st.success("Data saved!")

if selected == "Visualization":
    st.header("Visualization")
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

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Income", f"{total_income} {currency}")
            col2.metric("Total Expense", f"{total_expense} {currency}")
            col3.metric("Remaining Budget", f"{remaining_budget} {currency}")

            col4, col5 = st.columns(2)
            
            fig_incomes = px.pie(values=list(incomes.values()), names=list(incomes.keys()), title="Income Chart")
            col4.plotly_chart(fig_incomes, use_container_width=True)

            fig_expenses = px.pie(values=list(expenses.values()), names=list(expenses.keys()), title='Expense Chart')
            col5.plotly_chart(fig_expenses, use_container_width=True)

            st.text(f"Comment: {comment}")
        ###    