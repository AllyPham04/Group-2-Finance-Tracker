import streamlit as st 
import pandas as pd
import os
import plotly.express as px
import calendar
from millify import millify
from datetime import timedelta
from datetime import datetime
from config import *


def home():
    st.title(page_title + " " + page_icon)

    try:
        df = pd.read_csv('data.csv', parse_dates=['Date'], dayfirst=True)
        #df['Date'] = pd.to_datetime(df['Date'], format="%d-%m-%Y")
        df['Date'] = df['Date'].dt.date
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df = pd.DataFrame(columns=['Type', 'Date', 'Category', 'Amount'])

    display = st.columns([3, 1])
    display_r1 = display[0].columns(4)

    if os.path.exists('data.csv'):
        total_income = df[df['Type'] == 'Income']['Amount'].sum()
        total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
        total_balance = total_income - total_expense
        total_saving = df[(df['Type'] == 'Income') & (df['Category'] == 'Saving')]['Amount'].sum()
    else:
        total_income = 0
        total_expense = 0
        total_balance = 0
        total_saving = 0

    with display_r1[0]:
        total_balance_millified = millify(total_balance, precision=2)
        with st.container():
            st.subheader("Total Credits") 
            st.metric('Balance', f"{currency} {total_balance_millified}")

    with display_r1[1]:
        total_income_millified = millify(total_income, precision=2)
        with st.container():
            st.subheader("Total Income") 
            st.metric('Income', f"{currency} {total_income_millified}")

    with display_r1[2]:
        total_expense_millified = millify(total_expense, precision=2)
        with st.container():
            st.subheader("Total Expense") 
            st.metric('Expense', f"{currency} {total_expense_millified}")

    with display_r1[3]:
        total_saving_millified = millify(total_saving, precision=2)
        with st.container():
            st.subheader("Total Saving") 
            st.metric('Saving', f"{currency} {total_saving_millified}")

    button_left = display_r1[0].button("Next Week")
    button_right = display_r1[1].button("Last Week")
    current_date = datetime.now()

    if 'start_date' not in st.session_state:
        st.session_state['start_date'] = current_date - timedelta(days=(current_date.weekday() - 0) % 7)
        st.session_state['start_date'] = st.session_state['start_date'].date()

    if 'weekly_data' not in st.session_state:
        st.session_state['weekly_data'] = pd.DataFrame()
        weekly_data = st.session_state['weekly_data']

    displayr2 = display[0].columns([2, 1])
    with displayr2[0]:
        st.write('')
        st.write('')
        st.write('')
        with st.container():
            st.subheader("Weekly Chart")
            
            home_chart = st.selectbox('Chart', ['Bar Chart', 'Line Chart'])
            if button_left:
                st.session_state['start_date'] += timedelta(weeks=1)
            
            if button_right:
                st.session_state['start_date'] -= timedelta(weeks=1)

            date_range = pd.date_range(start=st.session_state['start_date'], periods=7)
            weekly_data = df[(df['Date'] >= st.session_state['start_date']) & (df['Date'] < st.session_state['start_date'] + timedelta(weeks=1))]
            
            all_days_data = pd.DataFrame({'Date': date_range})
            all_days_data['Date'] = pd.to_datetime(all_days_data['Date']).dt.date

            df_resampled = weekly_data.groupby(['Date', 'Type'])['Amount'].sum()
            df_resampled = df_resampled.reset_index()
            df_resampled['Type'] = pd.Categorical(df_resampled['Type'], categories=['Income', 'Expense'], ordered=True)
                
            all_days_data = pd.MultiIndex.from_product([all_days_data['Date'], ['Income', 'Expense']], names=['Date', 'Type']).to_frame(index=False)
            
            df_resampled = pd.merge(all_days_data, df_resampled, on=['Date', 'Type'], how='left', sort=True)

            df_resampled['Amount'].fillna(0, inplace=True)
            
            if home_chart == 'Bar Chart':
                visual_bar = px.bar(df_resampled, x="Date", y="Amount", color="Type", barmode="group")
                st.plotly_chart(visual_bar, use_container_width=True)
            
            elif home_chart == 'Line Chart':
                visual_line = px.line(df_resampled, x="Date", y="Amount", color="Type")
                st.plotly_chart(visual_line, use_container_width=True)

    with displayr2[1]:
        with st.container():
            all_income, all_expenses = st.tabs(["Income", "Expense"])
            with all_expenses:
                st.subheader("All Expense")

                weekly_expenses = weekly_data[weekly_data['Type'] == 'Expense']
                
                st.write('')
                st.write('')
                st.write('')
                st.write('')
                #all_days_data = pd.DataFrame({'Date': date_range})
                if not weekly_expenses.empty:
                    expenses_by_category = weekly_expenses.groupby('Category')['Amount'].sum().reset_index()

                    visual_pie = px.pie(expenses_by_category, values='Amount', names='Category', hole=0.5)
                    st.plotly_chart(visual_pie, use_container_width=True)
                else:
                    st.warning("No expense data available for the selected week.")
            
            with all_income:
                st.subheader("All Income")
                weekly_income = weekly_data[weekly_data['Type'] == 'Income']

                st.write('')
                st.write('')
                st.write('')
                st.write('')
                if not weekly_income.empty:
                    income_by_category = weekly_income.groupby('Category')['Amount'].sum().reset_index()

                    visual_pie = px.pie(income_by_category, values='Amount', names='Category', hole=0.5)
                    st.plotly_chart(visual_pie, use_container_width=True)
                else:
                    st.warning("No income data available for the selected week.")

    with display[1]:
        st.subheader('Goal Tracking')

        # Tạo danh sách các mission
        missions = ["Daily Login", "Necessity account",
                "Financial freedom account", "Education account",
                "Long-term saving for spending account"]
        sub_text = ['You add transactions everyday','<= 55% Income',
                    '~ 10% Income','~ 10% Income','~ 10% Income']

        # Hiển thị danh sách các mission
        st.markdown("Choose financial goals that you've achieved:")

        if 'earned_achievement' not in st.session_state:
            st.session_state['earned_achievement'] = set()

        if os.path.exists('daily_login.txt'):
            with open('daily_login.txt', 'r') as f:
                lines = f.readlines()
                last_clicked_mis1 = datetime.strptime(lines[0].strip(), '%Y-%m-%d').date()
                current_streak = int(lines[1])
        else:
            last_clicked_mis1 = None
            current_streak = 0

        if os.path.exists('necessity_acc.txt'):
            with open('necessity_acc.txt', 'r') as f:
                last_clicked_mis2 = datetime.strptime(f.read(), '%Y-%m-%d').date()
        else:
            last_clicked_mis2 = None
        
        if os.path.exists('financial_acc.txt'):
            with open('financial_acc.txt', 'r') as f:
                last_clicked_mis3 = datetime.strptime(f.read(), '%Y-%m-%d').date()
        else:
            last_clicked_mis3 = None
        
        if os.path.exists('education_acc.txt'):
            with open('education_acc.txt', 'r') as f:
                last_clicked_mis4 = datetime.strptime(f.read(), '%Y-%m-%d').date()
        else:
            last_clicked_mis4 = None
        
        if os.path.exists('long_term_saving.txt'):
            with open('long_term_saving.txt', 'r') as f:
                last_clicked_mis5 = datetime.strptime(f.read(), '%Y-%m-%d').date()
        else:
            last_clicked_mis5 = None

        now = datetime.now()

        first_day_of_month = datetime(now.year,now.month,1).date()
        _, last_day = calendar.monthrange(now.year,now.month)
        last_day_of_month = datetime(now.year,now.month,last_day).date()

        monthly_df = df.copy()

        monthly_df = monthly_df[(monthly_df['Date'] >= first_day_of_month) & (monthly_df['Date'] <= last_day_of_month)]

        today_df = monthly_df.copy()

        #In ra data theo tháng hiện tại mà đã nhóm vào từng Category
        monthly_df = monthly_df.groupby(['Type', 'Category'])['Amount'].sum().reset_index()

        today = now.date()
        today_df = today_df[today_df['Date'] == today]

        #Nhiem vu 1: Daily Login
        if st.checkbox('Daily Login'):
            st.write('You add transactions everyday.')

            # Check if a new month has started
            if last_clicked_mis1 is not None and last_clicked_mis1.month < today.month:
                current_streak = 0

            if today_df.empty:
                st.error('You haven\'t achieved this goal! Keep working!')
            elif last_clicked_mis1 == today:
                st.error('You have already clicked this checkbox today! Move to another goal')
            # If the user logged in yesterday
            elif last_clicked_mis1 == today - timedelta(days=1):
                current_streak += 1
            else:
                current_streak = 1
                with open('daily_login.txt', 'w') as f:
                    f.write(str(today) + '\n')  # Save the date when the checkbox was clicked
                    f.write(str(current_streak))
            if current_streak >= 10:
                st.success('Congratulations! You have earned the "Loyal User" achievement.')
                mis1 = f'{calendar.month_name[now.month]}/{now.year} - Loyal User'
                st.session_state['earned_achievement'].add(mis1)
            
        food_expenses = float(monthly_df[monthly_df['Category'] == 'Food']['Amount'].sum())

        clothes_expense = float(monthly_df[monthly_df['Category'] == 'Clothes']['Amount'].sum())

        trans_exp = float(monthly_df[monthly_df['Category'] == 'Transportation']['Amount'].sum())

        util_exp = float(monthly_df[monthly_df['Category'] == 'Utilities']['Amount'].sum())

        income_month = float(monthly_df[monthly_df['Type']=='Income']['Amount'].sum())

        #Nhiem vu 2: Necessity account
        if st.checkbox('Necessity account'):
            mis2 = f'{calendar.month_name[now.month]}/{now.year} - Essential Saver'
            st.write('Your monthly expense (food, transportation, etc.) is no larger than 55% of your income.')
            if last_clicked_mis2 is not None and first_day_of_month <= last_clicked_mis2 <= last_day_of_month:
                st.error('You have already clicked this checkbox this month! Move to another goal')

            if not 0 < (food_expenses + clothes_expense + util_exp + trans_exp) <= (0.55)*income_month:
                st.error('You haven\'t achieved this goal! Keep working!')
                if mis2 in st.session_state['earned_achievement']:
                    st.session_state['earned_achievement'].remove(mis2)

            elif 0 < (food_expenses + clothes_expense + util_exp + trans_exp) <= (0.55)*income_month:
                st.success('Congratulations! You have earned the "Essential Saver" achievement.')
                st.session_state['earned_achievement'].add(mis2)
                with open('necessity_acc.txt', 'w') as f:
                    f.write(str(today))  # Save the date when the checkbox was clicked


        #Nhiem vu 3: Financial freedom account

        invest_exp = float(monthly_df[monthly_df['Category'] == 'Investment']['Amount'].sum())

        if st.checkbox("Financial freedom account"):
            mis3 = f'{calendar.month_name[now.month]}/{now.year} - Investor\'s Edge'
            st.write('Your expense for investment is about 10% of your income.')
            if last_clicked_mis3 is not None and first_day_of_month <= last_clicked_mis3 <= last_day_of_month:
                st.error('You have already clicked this checkbox this month! Move to another goal')

            if not 0 < invest_exp <= income_month*0.1:
                st.error('You haven\'t achieved this goal! Keep working!')
                if mis3 in st.session_state['earned_achievement']:
                    st.session_state['earned_achievement'].remove(mis3)

            elif 0 < invest_exp <= income_month*0.1:
                st.success('Congratulations! You have earned the "Investor\'s Edge" achievement.')
                st.session_state['earned_achievement'].add(mis3)
                with open('financial_acc.txt', 'w') as f:
                    f.write(str(today))  # Save the date when the checkbox was clicked
                
        #Nhiem vu 4: Education account

        edu_exp = float(monthly_df[monthly_df['Category']=='Education']['Amount'].sum())

        if st.checkbox("Education account"):
            mis4 = f'{calendar.month_name[now.month]}/{now.year} - Academic Aces'
            st.write('Your expense for education is about 10% of your income.')
            if last_clicked_mis4 is not None and first_day_of_month <= last_clicked_mis4 <= last_day_of_month:
                st.error('You have already clicked this checkbox this month! Move to another goal')
                
            if not 0 < edu_exp <= 0.1 * income_month:
                st.error('You haven\'t achieved this goal! Keep working!')
                if mis4 in st.session_state['earned_achievement']:
                    st.session_state['earned_achievement'].remove(mis4)
            elif 0 < edu_exp <= 0.1 * income_month:
                st.success('Congratulations! You have earned the "Academic Aces" achievement.')
                st.session_state['earned_achievement'].add(mis4)
                with open('education_acc.txt', 'w') as f:
                    f.write(str(today))  # Save the date when the checkbox was clicked

                
        #Nhiem vu 5: Long-term saving

        saving_exp = float(monthly_df[monthly_df['Category'] == 'Saving']['Amount'].sum())

        if st.checkbox("Long-term saving for spending account"):
            mis5 = f'{calendar.month_name[now.month]}/{now.year} - Future Fortune Fund'
            st.write('Your saving is about 10% of your income.')
            if last_clicked_mis5 is not None and first_day_of_month <= last_clicked_mis5 <= last_day_of_month:
                st.error('You have already clicked this checkbox this month! Move to another goal')
                
            if not 0 < saving_exp <= 0.1*income_month:
                st.error('You haven\'t achieved this goal! Keep working!')
                if mis5 in st.session_state['earned_achievement']:
                    st.session_state['earned_achievement'].remove(mis5)

            elif 0 < saving_exp <= 0.1*income_month:
                st.success('Congratulations! You have earned the "Future Fortune Fund" achievement.')
                st.session_state['earned_achievement'].add(mis5)
                with open('long_term_saving.txt', 'w') as f:
                    f.write(str(today))  # Save the date when the checkbox was clicked
        
        st.subheader('Achievement')
        for achievement in st.session_state['earned_achievement']:
            st.write(f'- {achievement}')