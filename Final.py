import datetime as dt
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit_option_menu import option_menu
from config import *
from About_Us import info
from Home import home
from Set_budget import budget
from Tracker import track
from Report import rep
from Rewind import rewind, not_rewind

st.set_page_config(page_title='KEEPEE', page_icon='💸', layout=layout)

with st.sidebar:
    selected = option_menu(
            menu_title=None,  # required
            options=["About Us", "Home", "Set Budget", "Tracker", "Report", f"{dt.datetime.now().year} Rewind"],
            icons=["info", "house", "calculator", "database", "bar-chart-fill"],
            default_index=0,  # optional
            styles={
                "container": {"padding": "0!important", "background-color": "#FFFFFF"},
                "icon": {"color": "#42B781", "font-size": "18px"},
                "nav-link": {
                    "font-size": "18px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#A4D2C1",
                    "font-family": "Candara",
                },
                "nav-link-selected": {"background-color": "#519079"},
                },
            )
    with st.form(key='email_form'):

        st.markdown('''Whenever you have any problems, please let us know using the inbox below!''')
        st.markdown('''Before send email, going to your Google Account settings, clicking on \'Security\', 
                    and then turning on \'Less secure app access\'.''')

        email_sender = st.text_input('Your Email')
        password = st.text_input('Password', type="password")
        title = st.text_input('Title')
        body = st.text_input('Body')

        submit_button = st.form_submit_button('Send Email')
        if submit_button:
            try:
                # Create the email
                msg = MIMEMultipart()
                msg['From'] = email_sender
                msg['To'] = 'phamngoclinh3122004@gmail.com'
                msg['Subject'] = title
                msg.attach(MIMEText(body))

                #Create the SMTP server
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(email_sender, password)

                # Send the email
                s.send_message(msg)
                st.success('Your error report has been sent successfully.')

                s.quit()

            except Exception as error:
                st.error(f'An error occurred while sending the error report: {error}')

if selected == "About Us":
    info()

elif selected == "Home":
    home()

elif selected == "Set Budget":
    budget()

elif selected == "Tracker":
    track()

elif selected == "Report":
    rep()

elif selected == f"{dt.datetime.now().year} Rewind":
    if dt.datetime.now().month >= 11:
        rewind()
    else: not_rewind()
