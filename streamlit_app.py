import streamlit as st
import sqlalchemy
from sqlalchemy import create_engine
import geopandas as gpd
import matplotlib

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

user = st.secrets["p_user"]
db_password = st.secrets["p_password"]


st.write(f"DB Username: {user}")

host = st.secrets["p_host"]
port = st.secrets["p_port"]
database = st.secrets["p_database"]
user = st.secrets["p_user"]
password = st.secrets["p_password"]
st.write(f"DB Username: {user}")


db_connection_url = f"postgresql://student:{password}@158.193.56.170/postgis_33_sample"
con = create_engine(db_connection_url) 
sql = "SELECT * FROM hranice_okresy_1"

gdf = gpd.read_postgis(sql, con, geom_col='geom', crs = 5514)
gdf.plot()
