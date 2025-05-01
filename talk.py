import streamlit as st
import random
import time

st.write("Streamlit loves LLMs! 🤖 [Build your own chat app](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps) in minutes, then make it powerful by adding images, dataframes, or even input widgets to the chat.")

st.caption("Note that this demo app isn't actually connected to any LLMs. Those are expensive ;)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting! 👇"}]


def flip(id):
    if st.session_state[f"check{id}"]:
        st.session_state[f"box{id}"] = True
    else:
        st.session_state[f"box{id}"] = False

st.session_state["box0"] = False

# Display chat messages from history on app rerun
for message in st.session_state.messages:
        if message["role"] == "user":
            with st.container():
                col1, col2 = st.columns([8, 1])
                with col1:
                    st.chat_message("user").write(message["content"])
                with col2:
                    st.chat_message("user").checkbox(f"box{message['keyid']}", value=st.session_state[f"box{message['keyid']}"], key=f"check{message['keyid']}", on_change=flip, args=(message['keyid'],))
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    # Display user message in chat message container
    if "messages" in st.session_state:
        newid = len(st.session_state.messages)
    else:
        newid = 0
    st.session_state[f"box{newid}"] = False
    with st.container():
        col1, col2 = st.columns([8,1])
        with col1:
            st.chat_message("user").write(prompt)
        with col2:
            cb = st.chat_message("user").checkbox(f"box{newid}", value=st.session_state[f"box{newid}"], key=f"check{newid}", on_change=flip, args=(newid,))
            st.write(st.session_state[f"box{newid}"])
    st.session_state.messages.append({"role": "user", "content": prompt, "keyid": newid, "selected": cb})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = random.choice(
            [
                "Hmm that could use some more work",
                "That's an idea! Would you like me to send it to be collected?",
            ]
        )
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
