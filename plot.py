import pandas as pd
import streamlit as st
from psycopg2 import pool
from io import StringIO

connection_string = st.secrets.connections.neon['url']
conn_pool = pool.SimpleConnectionPool(1, 10, connection_string)
conn = conn_pool.getconn()
cur = conn.cursor()
cur.execute(f"""SELECT "data" FROM system WHERE "id" = 1""")
system = cur.fetchone()[0]

cur.execute(f"""SELECT "result" FROM results WHERE "phase" = {system['phase']} """)
raw = cur.fetchone()[0]
df = pd.DataFrame(raw)
df['idea_score'] = df['originality']*df['usefulness']
plotdf = df.groupby('user_id').agg({"is_idea": "sum", "idea_score": "max"})
st.header("Plot")
st.scatter_chart(plotdf, x="is_idea", y="idea_score")

st.write("Raw results")
st.write(df)