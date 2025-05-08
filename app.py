import streamlit as st
import re

# main_page = st.Page("data_summary.py", title="Samenvatting")
input_page = st.Page("talk.py", title="Brainstorm")
# ideas_page = st.Page("ideas.py", title="Ideas")
rate_page = st.Page("rate_ideas.py", title="Rating ideas")
plot_page = st.Page("plot.py", title="Plot ideas")

def valid_email(mailstr):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', mailstr)

def user_pin(pc):
    return pc == str(st.secrets.auth.pincode)

def admin_pin(pc):
    return pc == str(st.secrets.auth.admin_pincode)

if "name" in st.query_params and "pin" in st.query_params:
    st.session_state['name'] = st.query_params['name']
    st.session_state['pin'] = st.query_params['pin']

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
elif not user_pin(st.session_state.pin) and not admin_pin(st.session_state.pin):
    with st.form("logon_form"):
        st.header("Hi there! What is your e-mail address?")
        name = st.text_input("Your e-mail address", key="name")
        pincode = st.text_input("pincode", key="pin")
        st.markdown(''':red[Invalid pincode]''')
        submitted = st.form_submit_button("Enter")
else:
    st.session_state['name'] = st.session_state['name']
    st.session_state['pin'] = st.session_state['pin']
    if admin_pin(st.session_state.pin):
        pg = st.navigation([rate_page, plot_page, input_page])
    else:
        pg = st.navigation([input_page])
    pg.run()