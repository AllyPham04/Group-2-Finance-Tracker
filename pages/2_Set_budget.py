from 3_Tracker import total_expense

import streamlit as st

st.title("Set Budget ")

budget = st.number_input("Set Your Buget :", min_value=0.0, step=100.0)

if budget > 0:
    st.write(f"Bạn đã đặt ngân sách là: ${budget}")

if total_expense > budget :
    st.warning(f" bạn đã sử dụng quá :$ ")
