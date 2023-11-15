from _3_Tracker import *

import streamlit as st

st.title("Set Budget ")

budget = st.number_input("Set Your Buget :", min_value=0.0, step=100.0)

if budget > 0:
    st.write(f"your budget is : ${budget}")

if total_expense > budget :
    st.warning(f" over budget :${total_expense-budget} ")
    