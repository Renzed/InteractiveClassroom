import streamlit as st

for i, id in enumerate(st.session_state['ideas']):
    with st.container(border=True):
        st.subheader(f"Idea {i+1}", divider=True)
        st.write(st.session_state.messages[id]["content"])