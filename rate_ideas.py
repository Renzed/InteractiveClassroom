import streamlit as st
import pandas as pd
from pydantic import BaseModel
import enum
import time
from psycopg2 import pool
from google import genai
import asyncio
from io import StringIO
from tenacity import retry, wait_random_exponential, stop_after_delay

class Grade(enum.Enum):
    FIVE = "5"
    FOUR = "4"
    THREE = "3"
    TWO = "2"
    ONE = "1"

class IdeaRating(BaseModel):
    message_id: int
    is_idea: bool
    originality: Grade
    usefulness: Grade

connection_string = st.secrets.connections.neon['url']
conn_pool = pool.SimpleConnectionPool(1, 10, connection_string)
conn = conn_pool.getconn()
cur = conn.cursor()
cur.execute(f"""SELECT "data" FROM system WHERE "id" = 1""")
system = cur.fetchone()[0]
with open("system_instructions/" + system['phase'] + "processing.txt", "rb") as f:
    system_instruction = f.read().decode("UTF-8")

st.header("Idea rating")
if "start_rating" in st.query_params:
    st.write("Starting rating...")
    cur.execute(f"""SELECT * FROM chat_logs""")
    raw = cur.fetchall()
    # pre_df = [[6,"test@test.de","I have 2 dogs"],[6,"test@test.de","How many paws are in my house?"],[6,"test@test.de","I now have 3 dogs in my house"],[6,"test@test.de","Please don't count my feet as paws"],[6,"test@test.de","My name is John"],[6,"test@test.de","What is my name?"],[7,"philipeskenazi@hotmail.com","Hello"],[7,"philipeskenazi@hotmail.com","Airplane with banner "],[7,"philipeskenazi@hotmail.com","Tulips"],[7,"philipeskenazi@hotmail.com","A children's choir"],[7,"philipeskenazi@hotmail.com","I'm out of ideas"],[7,"philipeskenazi@hotmail.com","Nothing"]]
    pre_df = [(user_id, user, message_obj['content']) for user_id, user, messages_obj in raw for message_obj in messages_obj if message_obj['role'] == "user"]
    # st.write(pre_df)
    df = pd.DataFrame(pre_df, columns=["user_id","user","message"])
    df['message_id'] = df.index
    uid_list = df["user_id"].unique().tolist()
    # st.write(df)
    # st.write(df[["message_id","user_id","message"]].to_json(orient='records'))

    @retry(wait=wait_random_exponential(multiplier=1, min=0.5, max=10), stop=stop_after_delay(10))
    async def rate_ideas(tasknum, user_id):
        await asyncio.sleep(st.secrets.ai.gemini.fast_delay_seconds*tasknum)
        client = genai.Client(api_key=st.secrets.ai.gemini.key)
        response = await client.aio.models.generate_content(
            model=st.secrets.ai.gemini.model,
            contents=system_instruction + f" Rate all messages with user_id {user_id}. Please use the following JSON input: " + df[["message_id","user_id","message"]].to_json(orient='records'),
            config={
                'response_mime_type': 'application/json',
                'response_schema': list[IdeaRating],
            },
        )
        return response.text

    async def async_rate_ideas():
        # get_responses = [rate_ideas(i, 7) for i in range(20)]
        get_responses = [rate_ideas(i, uid) for (i, uid) in zip(range(20), uid_list)]
        return await asyncio.gather(*get_responses, return_exceptions=True)


    t0 = time.time()
    responses = asyncio.run(async_rate_ideas())
    t1 = time.time()
    st.write(t1-t0)
    # st.write(responses)
    #
    # st.write([type(i) for i in responses])
    # st.write([type(i)==str for i in responses])

    # for i in range(30):
    #     client = genai.Client(api_key=st.secrets.ai.gemini.key)
    #     response = client.models.generate_content(
    #         model=st.secrets.ai.gemini.model,
    #         contents=system_instruction + f" Rate all messages with user_id {7}. Please use the following JSON input: " + df[["message_id","user_id","message"]].to_json(orient='records'),
    #         config={
    #             'response_mime_type': 'application/json',
    #             'response_schema': list[IdeaRating],
    #         },
    #     )

    indiv_response = """[
    {
        "message_id": 6,
        "is_idea": false,
        "originality": "1",
        "usefulness": "1"
    },
    {
        "message_id": 7,
        "is_idea": true,
        "originality": "3",
        "usefulness": "4"
    },
    {
        "message_id": 7,
        "is_idea": true,
        "originality": "3",
        "usefulness": "2"
    },
    {
        "message_id": 8,
        "is_idea": true,
        "originality": "3",
        "usefulness": "3"
    },
    {
        "message_id": 9,
        "is_idea": true,
        "originality": "4",
        "usefulness": "4"
    },
    {
        "message_id": 10,
        "is_idea": false,
        "originality": "1",
        "usefulness": "1"
    },
    {
        "message_id": 11,
        "is_idea": false,
        "originality": "1",
        "usefulness": "1"
    }
]"""

    dfs = [df.merge(pd.read_json(StringIO(response)).drop_duplicates(subset=["message_id"]),on="message_id") for response in responses if type(response)==str]
    response_df = pd.concat(dfs)
    st.write(response_df)

    q = f"""INSERT INTO results ("phase", "result") VALUES ({system['phase']}, %s) ON CONFLICT ("phase") DO UPDATE SET "result" = %s"""
    # q = f"""INSERT INTO results ("phase", "result") VALUES ({system['phase']}, %s)"""
    cur.execute(q, (response_df.to_json(orient='records'),response_df.to_json(orient='records')))
    conn.commit()
    conn.close()
    time.sleep(3)
    st.switch_page("plot.py")