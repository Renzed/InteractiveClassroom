import streamlit as st

def remove_idea(id):
    st.session_state[f'box{id}'] = False
    st.session_state['ideas'].remove(id)

for i, id in enumerate(st.session_state['ideas']):
    with st.container(border=True):
        col1, col2 = st.columns([8,1])
        with col1:
            st.subheader(f"Idea {i+1}", divider=True)
            st.write(st.session_state.messages[id]["content"])
        with col2:
            st.button("", key=f"button{i}", on_click=remove_idea, args=(id,), icon=":material/delete:", use_container_width=True)