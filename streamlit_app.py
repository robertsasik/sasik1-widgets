import streamlit as st
import sqlalchemy
from sqlalchemy import create_engine
import geopandas as gpd
import matplotlib
import folium
from streamlit_folium import st_folium



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

@st.cache_resource
def get_db_connection():
    db_connection_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(db_connection_url) 
    return engine

con = get_db_connection()
sql = "SELECT * FROM hranice_okresy_1"
#sql = st.text_input("Zadaj SQL skript: ")

gdf = gpd.read_postgis(sql, con, geom_col='geom', crs = 5514)
gdf

#gdf = gdf.to_crs(epsg=4326)

m = folium.Map(location=[48.14816, 17.10674], zoom_start=8) 

def style_function(feature):
    return {
        'fillColor': '#3186cc',  # Farba výplne polygónov
        'color': 'black',        # Farba hrán polygónov
        'weight': 2,             # Hrúbka hrán
        'fillOpacity': 0.6,      # Priehľadnosť výplne (0-1)
    }

# Pridanie GeoDataFrame vrstvy na mapu so zvoleným štýlom
folium.GeoJson(gdf, style_function=style_function).add_to(m)

# Zobrazenie interaktívnej mapy v Streamlit
st_folium(m, width=800, height=600)