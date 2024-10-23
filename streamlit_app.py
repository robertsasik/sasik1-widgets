import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

user = st.secrets["p_user"]
db_password = st.secrets["p_password"]


st.write(f"DB Username: {user}")
