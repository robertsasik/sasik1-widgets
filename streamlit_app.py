import streamlit as st
import sqlalchemy
from sqlalchemy import create_engine
import geopandas as gpd
import matplotlib
import folium
from streamlit_folium import st_folium



st.title("🗺️Interaktivna mapa okresov🌍")
st.write(
    "Interaktívna mapa okresov SR pomocou frameworku streamlite a knižnice folium."
)

#Vytvorenie skrytých premenných na pripojenie do databázy
host = st.secrets["p_host"]
port = st.secrets["p_port"]
database = st.secrets["p_database"]
user = st.secrets["p_user"]
password = st.secrets["p_password"]
st.write(f"DB Username: {user}")

@st.cache_resource #dekorátor pripojenia na databázové zdroje

#Vytvorenie funkcie na pripojenie na databázu
def get_db_connection():
    db_connection_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(db_connection_url) 
    return engine

#Volanie funkcie pomocou premennej con
con = get_db_connection()

#SQL dopyt pomocou premennej sql
sql = "SELECT * FROM hranice_okresy_1"

#Pužitie geopandas na volanie relačnej tabuľky z PostgreSQL+Postgis databázy
gdf = gpd.read_postgis(sql, con, geom_col='geom', crs = 5514)
gdf

#Konverzia súradnicového systému S-JTSK na WGS-84 pomocou geopandas
gdf = gdf.to_crs(epsg=4326)

#Vytvorenie interaktívnej mapy pomocou knižnice folium do objektu m
m = folium.Map(location=[48.705, 19.16], zoom_start=8) 

#Definícia štýlu vykreslenia polygónovej vrstvy
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