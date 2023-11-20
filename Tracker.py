import streamlit as st
import os
import calendar
import pandas as pd
import plotly.express as px
from config import *
from datetime import datetime
from millify import millify


def track():
    st.title("Tracker")
    col_a1, col_a2, col_a3 = st.columns([0.2, 0.4, 0.4], gap='small')
    #st.divider()
    col_b1, col_b2 = st.columns(2)

    now = datetime.now()

    _, last_day = calendar.monthrange(now.year, now.month)

    first_day_of_month = datetime(now.year, now.month, 1).date()
    last_day_of_month = datetime(now.year, now.month, last_day).date()

    total_income = 0
    total_expense = 0

    if 'previous_total_balance' not in st.session_state:
        st.session_state['previous_total_balance'] = 0

    previous_total_balance = st.session_state['previous_total_balance']

    with col_b1:
        tab1, tab2 = st.tabs(["Income", "Expense"])

        with tab1:
            with st.form("income", clear_on_submit=True):
                st.subheader("Transaction")
                selected_date = st.date_input("Select date:", value=now.date(), format="DD/MM/YYYY")
                amount = st.number_input(f"Amount:", min_value=0, format="%i", step=10)
                category = st.selectbox("Category:", incomes)
                if st.form_submit_button("Save Data"):
                    # Gather user inputs
                    user_data = {
                        'Type': 'Income',
                        'Date': selected_date.strftime("%d-%m-%Y"),
                        'Category': category,
                        'Amount': amount
                    }

                    try:
                        history_df = pd.read_csv('data.csv')
                    except (FileNotFoundError, pd.errors.EmptyDataError):
                        history_df = pd.DataFrame(columns=user_data.keys())

                    history_df = pd.concat([pd.DataFrame(user_data, index=[0]), history_df], ignore_index=True)
                    history_df['Date'] = pd.to_datetime(history_df['Date'], format="%d-%m-%Y")
                    history_df = history_df.sort_values(by=['Date'], ascending=False)
                    history_df.to_csv('data.csv', index=False, date_format="%d-%m-%Y")

                    st.success("Data saved!")

        with tab2:
            with st.form("expense", clear_on_submit=True):
                st.subheader("Transaction")
                selected_date = st.date_input("Select date:", value=now.date(), format="DD/MM/YYYY")
                amount = st.number_input(f"Amount:", min_value=0, format="%i", step=10)
                category = st.selectbox("Category:", expenses)
                if st.form_submit_button("Save Data"):
                    # Gather user inputs
                    user_data = {
                        'Type': 'Expense',
                        'Date': selected_date.strftime("%d-%m-%Y"),
                        'Category': category,
                        'Amount': amount
                    }

                    try:
                        history_df = pd.read_csv('data.csv')
                    except (FileNotFoundError, pd.errors.EmptyDataError):
                        history_df = pd.DataFrame(columns=user_data.keys())

                    history_df = pd.concat([pd.DataFrame(user_data, index=[0]), history_df], ignore_index=True)
                    history_df['Date'] = pd.to_datetime(history_df['Date'], format="%d-%m-%Y")
                    history_df = history_df.sort_values(by=['Date'], ascending=False)
                    history_df.to_csv('data.csv', index=False, date_format="%d-%m-%Y")

                    st.success("Data saved!")

    with col_b2:
        st.write('')
        st.write('')
        st.write('')
        with st.form("transactions_history", clear_on_submit=True):
            st.subheader("History")
            if os.path.exists('data.csv'):
                history_df = pd.read_csv('data.csv', parse_dates=True, dayfirst=True)
                total_income = history_df[history_df['Type'] == 'Income']['Amount'].sum()
                total_expense = history_df[history_df['Type'] == 'Expense']['Amount'].sum()
                total_balance = total_income - total_expense
                total_saving = history_df[(history_df['Type'] == 'Income') & (history_df['Category'] == 'Saving')]['Amount'].sum()
            else:
                history_df = pd.DataFrame()
                col3_df = history_df.copy()
                total_balance = 0
                total_saving = 0

            if not history_df.empty:
                col3_df['Amount'] = col3_df.apply(lambda row: row['Amount']
                                                    if row['Type'] == 'Income'
                                                    else row['Amount'] * -1, axis=1)


                monthly_df = history_df.copy() #monthly_data
                monthly_df['Date'] = pd.to_datetime(monthly_df['Date'], dayfirst=True).dt.date
                monthly_df = monthly_df[(monthly_df['Date'] >= first_day_of_month) & (monthly_df['Date'] <= last_day_of_month)]

                history_df.index = history_df.index + 1
                history_df['Amount'] = history_df.apply(lambda row: f'+ {currency} {row["Amount"]}' 
                                        if row['Type'] == 'Income' 
                                        else f'- {currency} {row["Amount"]}', axis=1)

                st.dataframe(history_df.drop(columns='Type'), use_container_width=True)
            
            
            if os.path.exists('budget.csv') and os.path.exists('data.csv'):
                budget_df = pd.read_csv('budget.csv')
                for expense in expenses:
                    if expense in budget_df['Category'].values:
                        budget_expense = float(budget_df[budget_df['Category'] == expense]['Budget'].values[0])
                        expense_cate = float(monthly_df[(monthly_df['Type'] == 'Expense') & (monthly_df['Category'] == expense)]['Amount'].sum())
                        if expense_cate > 0.9 * budget_expense:
                            if not st.session_state.get(f'warning_{expense}', False):
                                st.warning(f"You have spent over 90% of your budget for {expense} category in {calendar.month_name[now.month]}")
                                st.session_state[f'warning_{expense}'] = True
            else:
                pass

            #if st.form_submit_button("Clear all data"):
                #st.session_state.clear()
                #if os.path.exists('data.csv'):
                    #os.remove('data.csv')
                    #st.success("Data cleared!")
                #user_income.clear()
                #user_expense.clear()
    st.session_state['previous_total_balance'] = total_balance

    delta_balance = total_balance - previous_total_balance
    delta_balance_millified = millify(delta_balance, precision=2)

    with col_a1:
        total_balance_millified = millify(total_balance, precision=2)
        with st.container():
            st.subheader("Total Credits")
            st.metric('Balance', f"{total_balance_millified} {currency}", delta=f"{delta_balance_millified} {currency}", delta_color="normal")

    with col_a2:
        col_a2_1, col_a2_2 = st.columns(2)
        col_a2_1.subheader("Saving Goal")

        saving_goal = col_a2_1.number_input("Enter your saving goal:", min_value=0, format="%i", step=10)

        if col_a2_1.button("Save"):
            col_a2_1.write(f'Your saving goal is {saving_goal} {currency}')
            if total_saving >= saving_goal:
                st.success("Congratulations! You have reached your saving goal!")
            elif total_saving == 0:
                st.warning("You have not saved anything yet!")
            else:
                fig_saving = px.pie(values=[total_saving, saving_goal - total_saving],
                                    names=["Saving", "Remaning"],
                                    title=f'Saving Progress')
                col_a2_2.plotly_chart(fig_saving, use_container_width=True)

    with col_a3:
        st.subheader(f'Your balance in {datetime.now().year}')

        visual_df = col3_df.copy()
        visual_df['Date'] = pd.to_datetime(visual_df['Date'], format='%d-%m-%Y')
        visual_df['Month'] = visual_df['Date'].dt.strftime('%b')

        # Group by month and sum 'Amount' for each group
        grouped_data = visual_df.groupby('Month')['Amount'].sum().reset_index()

        # Create a DataFrame with all months in the desired range
        all_months = pd.date_range(start=f'{datetime.now().year}-01-01', end=f'{datetime.now().year}-12-31', freq='M')
        all_months_df = pd.DataFrame({'Date': all_months, 'Amount': 0})

        # Convert the 'Date' column to month names in all_months_df
        all_months_df['Month'] = all_months_df['Date'].dt.strftime('%b')

        # Merge the two DataFrames, filling missing values with 0
        result_df = pd.merge(all_months_df, grouped_data, on='Month', how='left').fillna(0)

        visual = px.line(
            result_df,
            x='Month',
            y='Amount_y',
            markers=True,
        )
        visual.update_layout(height=300, xaxis_title='Month', yaxis_title='Total Amount')
        st.plotly_chart(visual, use_container_width=True)