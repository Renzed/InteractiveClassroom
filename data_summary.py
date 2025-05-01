import streamlit as st
import pandas as pd
import numpy as np

ideas = np.random.randint(0,10,10)
good_ideas = (np.random.normal(1/3,0.01,10)*ideas).astype(int)
df = pd.DataFrame({
    'ideën': ideas,
    'goeie ideën': good_ideas,
    'naam': ['Liam','Noah','Oliver','James','Elijah','Mateo','Theodore','Henry','Lucas','William']
}).set_index('naam')
st.write("Here's our first attempt at using data to create a table:")
st.write(df)

st.write(st.session_state)
st.write(st.session_state.messages)
