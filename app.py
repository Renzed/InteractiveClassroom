import streamlit as st

main_page = st.Page("data_summary.py", title="Samenvatting")
input_page = st.Page("talk.py", title="Brainstorm")

if "name" not in st.session_state:
    st.header("Hi there! What is your name?")
    name = st.text_input("Your name", key="name")
elif st.session_state['name'] == "":
    st.header("Hi there! What is your name?")
    name = st.text_input("Your name", key="name")
else:
    st.session_state['name'] = st.session_state['name']
    pg = st.navigation([main_page, input_page])
    pg.run()