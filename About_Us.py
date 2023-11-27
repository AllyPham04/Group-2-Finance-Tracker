import streamlit as st
from config import *

def info():
    tmp1, main_col, tmp2 = st.columns([1, 3, 1])

    with main_col:
        background_about_us()

        local_css('style.css')
        flake1 = "💸"

        st.markdown(
            f"""
            <div class="snowflake">{flake1}</div>
            <div class="snowflake">{flake1}</div>
            <div class="snowflake">{flake1}</div>
            <div class="snowflake">{flake1}</div>
            <div class="snowflake">{flake1}</div>
            <div class="snowflake">{flake1}</div>
            <div class="snowflake">{flake1}</div>
            <div class="snowflake">{flake1}</div>
            <div class="snowflake">{flake1}</div>
            <div class="snowflake">{flake1}</div>
            """,
            unsafe_allow_html=True)

        st.markdown(f"""<h1 style='text-align: center; 
                    font-family: {fontFamily}; 
                    font-size: 50px'>
                    {app_name}
                    </h1>""", unsafe_allow_html=True)

        col1_1, col1_2, col1_3 = st.columns([1,4,1])
        col1_2.image('slogan.png', use_column_width=True)

        st.markdown(f"""<h4 style='font-family: {fontFamily}; margin-top: -30px;'>Our Team</h4>""", unsafe_allow_html=True)
        col2_1, col2_2, col2_3, col2_4 = st.columns(4)
        with col2_1:
            linh_img = "linh.png"
            st.image(linh_img, use_column_width=True)

            style_text = f"""
                <div style="
                text-align: center; 
                margin-top: -30px;
                font-family: {fontFamily};
                ">
                <h3 style="margin: 0;">FOUNDER</h3>
                <h5 style="font-weight: lighter;">Pham Ngoc Linh</h5>
                </div>
            """
            st.markdown(style_text, unsafe_allow_html=True)

        with col2_2:
            nhi_img = "nhi.png"
            st.image(nhi_img, use_column_width=True)

            style_text = f"""
                <div style="
                text-align: center; 
                margin-top: -30px;
                font-family: {fontFamily};
                ">
                <h3 style="margin: 0;">FOUNDER</h3>
                <h5 style="font-weight: lighter;">Pham Ngoc Nhi</h5>
                </div>
            """
            st.markdown(style_text, unsafe_allow_html=True)

        with col2_3:
            banh_img = "banh.png"
            st.image(banh_img, use_column_width=True)

            style_text = f"""
                <div style="
                text-align: center; 
                margin-top: -30px;
                font-family: {fontFamily};">
                <h3 style="margin: 0;">FOUNDER</h3>
                <h5 style="font-weight: lighter;">Bui Ngoc Bao Anh</h5>
                </div>
            """
            st.markdown(style_text, unsafe_allow_html=True)

        with col2_4:
            tron_img = "tron.png"
            st.image(tron_img, use_column_width=True)

            style_text = f"""
                <div style="
                text-align: center; 
                margin-top: -30px;
                margin-bottom: 30px;
                font-family: {fontFamily};">
                <h3 style="margin: 0;">FOUNDER</h3>
                <h5 style="font-weight: lighter;">Nguyen Tuan Trong</h5>
                </div>
            """
            st.markdown(style_text, unsafe_allow_html=True)

        intro, gif = st.columns(2)
        with intro:
            st.subheader("Introduction")
            st.markdown(f"""<p style='text-align: justify; font-family: {fontFamily};'>
                                Welcome to the {app_name}! 
                                Where managing your finances becomes seamless and insightful.
                                Start your financial journey by recording transactions, 
                                setting goals, and gaining valuable insights into your spending habits. 
                                Empower yourself with smart financial decisions through our user-friendly interface. 
                                Happy tracking!
                                </p>""", unsafe_allow_html=True)

        with gif:
            st.image('throw-money.gif')
