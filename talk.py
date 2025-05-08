import streamlit as st
import time
from psycopg2 import pool
from google import genai
from google.genai import types
import json

connection_string = st.secrets.connections.neon['url']
conn_pool = pool.SimpleConnectionPool(1, 10, connection_string)
conn = conn_pool.getconn()
cur = conn.cursor()
user_email = st.session_state.name.lower()
cur.execute(f"SELECT * FROM chat_logs WHERE chat_logs.user = '{user_email}';")
dblist = cur.fetchall()
cur.execute(f"""SELECT "data" FROM system WHERE "id" = 1""")
system = cur.fetchone()[0]
with open('system_instructions/' + system['phase'] + 'chatting.txt','rb') as f:
    system_instruction = f.read().decode("UTF-8")

if len(dblist)==1:
    cur.execute(f"""SELECT "messages" FROM chat_logs WHERE "user" = '{user_email}'""")
    prev = cur.fetchone()[0]
    st.session_state.messages = prev
elif len(dblist)>1:
    raise ValueError("Only one user can exist")
else:
    st.write("nog geen db entry")
    cur.execute(f"""INSERT INTO chat_logs ("id", "user", "messages") VALUES (default, '{user_email}', '[]');""")
    conn.commit()
    if "messages" not in st.session_state:
        st.session_state.messages = []

history = [types.Content(role=message["role"], parts=[types.Part(text=message["content"])]) for message in st.session_state.messages]

gemini_client = genai.Client(api_key=st.secrets.ai.gemini.key)
gemini_chat = gemini_client.chats.create(
    model=st.secrets.ai.gemini.model,
    config=types.GenerateContentConfig(
        system_instruction=system_instruction),
    history=history
)


def update_messages():
    q = f"""UPDATE chat_logs SET "messages" = %s WHERE "user" = '{user_email}'"""
    cur.execute(q, (json.dumps(st.session_state.messages),))
    conn.commit()

st.header("Let's brainstorm!")

st.caption("")


# Display chat messages from history on app rerun
for message in st.session_state.messages:
        with st.chat_message(message["role"]):
                st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    # Display user message in chat message container
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt, "datetime": time.gmtime()})

    # Display assistant response in chat message container
    with st.chat_message("model"):
        full_response = ""
        tokens_used = 0
        message_placeholder = st.empty()
        response = gemini_chat.send_message_stream(message=prompt)
        for chunk in response:
            full_response += chunk.text
            message_placeholder.markdown(full_response)
            tokens_used += chunk.usage_metadata.total_token_count
        st.write(tokens_used)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "model", "content": full_response})
    update_messages()

# st.write(gemini_chat.get_history())