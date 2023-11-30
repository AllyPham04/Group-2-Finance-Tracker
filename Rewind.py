import streamlit as st
import datetime as dt
from config import *
import pandas as pd

def not_rewind():
    st.title("It's not the end of the year yet, comes back later on December")

def rewind():
    # ---------------------------------------------------------------------------
    local_css('style.css')
    background_about_us()
    try:
        history_df = pd.read_csv('data.csv')
    except (FileNotFoundError, pd.errors.EmptyDataError):
        history_df = pd.DataFrame(columns=['Type', 'Date', 'Category', 'Amount', 'Note'])
    # ---------------------------------------------------------------------------
    if not history_df.empty:
        cate_amount_df = history_df.groupby('Type')['Category'].count().reset_index()
        amount_income = cate_amount_df[cate_amount_df['Type'] == 'Income']
        if not amount_income.empty:
            count_income = amount_income['Category'].iloc[0]
        else:
            count_income = 0
        amount_expense = cate_amount_df[cate_amount_df['Type'] == 'Expense']
        if not amount_expense.empty:
            count_expense = amount_expense['Category'].iloc[0]
        else:
            count_expense = 0
        # ---------------------------------------------------------------------------
        num_row = history_df.shape[0]
        # ---------------------------------------------------------------------------
        index_of_max_amount = history_df['Amount'].idxmax()
        # ---------------------------------------------------------------------------
        # Retrieve the row with the highest amount
        row_with_max_amount = history_df.loc[index_of_max_amount]
        highest_amount = '{:,.0f}'.format(row_with_max_amount['Amount'])
        # ---------------------------------------------------------------------------
        type_counts = history_df['Category'].value_counts()
        highest_count = type_counts.get(row_with_max_amount['Category'], 0)
        #---------------------------------------------------------------------------
        income_df = history_df[history_df['Type'] == 'Income']
        expense_df = history_df[history_df['Type'] == 'Expense']
        top_income = income_df.nlargest(5, 'Amount')
        top_expense = expense_df.nlargest(5, 'Amount')
        # ---------------------------------------------------------------------------
        date_count = history_df['Date'].nunique()
        # ---------------------------------------------------------------------------
        count_cate = history_df.groupby('Category')['Amount'].count().reset_index().sort_values(by='Amount', ascending=False)
        sum_count_cate = history_df.groupby('Category')['Amount'].sum().reset_index()
        sum_count_cate = sum_count_cate[sum_count_cate['Category'] == count_cate.iloc[0]['Category']]
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        curr_year = dt.datetime.now().year
        ss = st.session_state
        logo_font_size = "60px"
        title_font_size = "50px"
        subheader_font_size = "30px"

        def rew1():
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.markdown(f"""<h1 style='
            text-align: center; 
            font-family: {fontFamily}; 
            font-size: {title_font_size}
            '>
            {curr_year} Rewind
            </h1>""", unsafe_allow_html=True)

            st.markdown(f"""<h1 style='
                    text-align: center; 
                    font-family: {fontFamily}; 
                    font-size: {logo_font_size};
                    font-weight: lighter
                    '>
                    KEEPEE
                    </h1>""", unsafe_allow_html=True)


        def rew2():
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {subheader_font_size};
                        font-weight: normal;
                        '>
                        Hello KEEPEE's User
                        </h1>""", unsafe_allow_html=True)


        def rew3():
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')

            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {subheader_font_size};
                        font-weight: normal;
                        '>
                        Hello KEEPEE's User
                        </h1>""", unsafe_allow_html=True)

            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {subheader_font_size};
                        font-weight: normal;
                        '>
                        It's Rewind time.<br>
                        Ready? Let's do this.
                        </h1>""", unsafe_allow_html=True)

        def rew4():
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {title_font_size}
                        '>
                        {curr_year} was a feast <br> for your wallet
                        </h1>""", unsafe_allow_html=True)

        def rew5():
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')

            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {title_font_size}
                        '>
                        {curr_year} was a feast <br> for your wallet
                        </h1>""", unsafe_allow_html=True)

            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {subheader_font_size};
                        font-weight: normal;
                        '>
                        Your Income comes from {count_income} categories <br>
                        and {count_expense} for Expense
                        </h1>""", unsafe_allow_html=True)

        def rew6():
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')

            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {title_font_size}
                        '>
                        You made {num_row} transactions <br> in {curr_year}
                        </h1>""", unsafe_allow_html=True)

            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {subheader_font_size};
                        font-weight: normal;
                        '>
                        And there was one that really 'connected'.
                        </h1>""", unsafe_allow_html=True)

        def rew7():
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {title_font_size}
                        '>
                        Your top transaction was {row_with_max_amount['Category']} with {highest_amount} {currency}
                        </h1>""", unsafe_allow_html=True)

            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {subheader_font_size};
                        font-weight: normal;
                        '>
                        You also made it {highest_count} times,
                        starting at {row_with_max_amount['Date']}.
                        </h1>""", unsafe_allow_html=True)

        def rew8():
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {title_font_size}
                        '>
                        But you had space in your purse for more than one favorite
                        </h1>""", unsafe_allow_html=True)

        def rew9():
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.markdown(f"""<h1 style='
                        text-align: left; 
                        font-family: {fontFamily}; 
                        font-size: {title_font_size}
                        '>
                        Your top transaction
                        </h1>""", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(top_income.set_index(keys='Type'))

            with col2:
                st.dataframe(top_expense.set_index(keys='Type'))

        def rew10():
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {title_font_size}
                        '>
                        Time is a construct, but we kept track anyway
                        </h1>""", unsafe_allow_html=True)

        def rew11():
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {title_font_size}
                        '>
                        You used KEEPEE for <br> {date_count} days
                        </h1>""", unsafe_allow_html=True)

            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {subheader_font_size};
                        font-weight: normal;
                        '>
                        That is truly a long period of time.
                        </h1>""", unsafe_allow_html=True)

        def rew12():
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {title_font_size}
                        '>
                        You made up {count_income + count_expense} categories this year, but one came out on top
                        </h1>""", unsafe_allow_html=True)

            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {subheader_font_size};
                        font-weight: normal;
                        '>
                        Any guesses?
                        </h1>""", unsafe_allow_html=True)

        def rew13():
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {title_font_size}
                        '>
                        Say hello to your top category, <br>
                        {count_cate.iloc[0]['Category']}
                        </h1>""", unsafe_allow_html=True)

            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {subheader_font_size};
                        font-weight: normal;
                        '>
                        You used this category {count_cate.iloc[0]['Amount']} times 
                        and spending {'{:,.0f}'.format(sum_count_cate.iloc[0]['Amount'])} {currency} on it.
                        </h1>""", unsafe_allow_html=True)

        def rew14():
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.markdown(f"""<h1 style='
                        text-align: center; 
                        font-family: {fontFamily}; 
                        font-size: {title_font_size}
                        '>
                        That's it, thank you for accompanying KEEPEE throughout 
                        the past year. KEEPEE hopes that all the good things will come to you.
                        </h1>""", unsafe_allow_html=True)

        tmp1, main_col, tmp2 = st.columns([1, 2, 1])
        with main_col:

            story_rewind = [
                rew1, rew2, rew3, rew4, rew5,
                rew6, rew7, rew8, rew9, rew10,
                rew11, rew12, rew13, rew14
            ]
            if 'index' not in ss:
                ss.index = 0
            post_position = st.slider("Swipe to view posts", 0, len(story_rewind) - 1)
            ss.index = post_position
            story_rewind[ss.index]()
    else:
        st.title("You haven't made any transactions yet, please come back later")