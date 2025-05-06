import streamlit as st
import re

main_page = st.Page("data_summary.py", title="Samenvatting")
input_page = st.Page("talk.py", title="Brainstorm")
ideas_page = st.Page("ideas.py", title="Ideas")

def valid_email(mailstr):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', mailstr)

def valid_pin(pc):
    return pc == str(st.secrets.auth.pincode)

if "name" not in st.session_state:
    with st.form("logon_form"):
        st.header("Hi there! What is your e-mail address?")
        name = st.text_input("Your e-mail address", key="name")
        pincode = st.text_input("pincode", key="pin")
        submitted = st.form_submit_button("Enter")
elif not valid_email(st.session_state.name):
    with st.form("logon_form"):
        st.header("Hi there! What is your e-mail address?")
        name = st.text_input("Your e-mail address", key="name")
        st.markdown(''':red[Not a valid e-mail adress]''')
        pincode = st.text_input("pincode", key="pin")
        submitted = st.form_submit_button("Enter")
elif not valid_pin(st.session_state.pin):
    with st.form("logon_form"):
        st.header("Hi there! What is your e-mail address?")
        name = st.text_input("Your e-mail address", key="name")
        pincode = st.text_input("pincode", key="pin")
        st.markdown(''':red[Invalid pincode]''')
        submitted = st.form_submit_button("Enter")
else:
    st.session_state['name'] = st.session_state['name']
    st.session_state['pin'] = st.session_state['pin']
    pg = st.navigation([input_page])
    pg.run()