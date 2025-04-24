import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px

# --- App Title ---
st.title("🇬🇧 Sound of the UK")
st.markdown("Explore how music tastes vary across UK cities using Spotify data: track trends, moods, and genre preferences.")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/uk_spotify_by_city.csv")  # Your dataset should have: city, lat, lon, track_name, artist, streams, danceability, energy, valence
    return df

data = load_data()

# --- Sidebar: City Filter ---
st.sidebar.header("Filter Options")
cities = sorted(data["city"].unique())
selected_city = st.sidebar.selectbox("Select a City", cities)

# --- Filtered Data ---
city_data = data[data["city"] == selected_city]

# --- City Overview ---
st.subheader(f"🎶 Top Tracks in {selected_city}")
top_tracks = city_data.groupby(["track_name", "artist"])["streams"].sum().reset_index().sort_values(by="streams", ascending=False).head(10)
st.dataframe(top_tracks)

# --- Mood Metrics ---
st.subheader("🎧 Mood Metrics")
avg_metrics = city_data[["danceability", "energy", "valence"]].mean().round(2)
st.metric("Danceability", avg_metrics["danceability"])
st.metric("Energy", avg_metrics["energy"])
st.metric("Valence (Happiness)", avg_metrics["valence"])

# --- Map of All Cities ---
st.subheader("🗺️ Map of UK Listening Trends")
map_df = data.groupby("city").agg({
    "lat": "first",
    "lon": "first",
    "streams": "sum"
}).reset_index()

uk_map = folium.Map(location=[54.5, -3], zoom_start=5)
for _, row in map_df.iterrows():
    popup = f"{row['city']}<br>Total Streams: {row['streams']}"
    folium.CircleMarker(
        location=(row['lat'], row['lon']),
        radius=7,
        popup=popup,
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.6
    ).add_to(uk_map)

folium_static(uk_map)

st.markdown("Data is representative and aggregated. Mood metrics are based on Spotify audio features per city.")
