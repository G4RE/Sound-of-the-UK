import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- Spotify Authentication ---
client_id = '78bdb3a079034abdb0ea7ed6df0ff528'
client_secret = 'dd79a32ec58d4e17a63241d8e597eba8'

# Set up Spotify API client with proper authentication
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# --- App Title ---
st.title("🇬🇧 Sound of the UK")
st.markdown("Explore how music tastes vary across UK cities using Spotify data: track trends, moods, and genre preferences.")

# --- Real-Time Data Fetching Function ---
@st.cache_data
def get_spotify_data():
    # Example: Fetching the top 10 tracks in the UK based on popularity or streams
    # Here, I'm getting tracks from a top chart playlist (e.g., 'Top 50 - United Kingdom')
    playlist_id = '37i9dQZEVXbLp5XoPON0wI'  # Spotify Playlist ID for 'Top 50 - United Kingdom'
    results = sp.playlist_tracks(playlist_id)
    
    # Extracting track names, artists, and streams (popularity)
    track_data = []
    for item in results['items']:
        track_name = item['track']['name']
        artist_name = item['track']['artists'][0]['name']
        popularity = item['track']['popularity']
        
        track_data.append({
            'Track': track_name,
            'Artist': artist_name,
            'Popularity': popularity
        })
    
    return pd.DataFrame(track_data)

# --- Load Real-Time Data ---
data = get_spotify_data()

# --- Display Real-Time Data ---
st.subheader("🎶 Real-Time Top Tracks in the UK")
st.dataframe(data)

# --- Mood Metrics (from Spotify data) ---
st.subheader("🎧 Mood Metrics for Tracks")
# Fetch audio features for the top track for demonstration
top_track = data['Track'].iloc[0]
track_uri = sp.search(q=top_track, type='track', limit=1)['tracks']['items'][0]['uri']
audio_features = sp.audio_features([track_uri])[0]

# Extract danceability, energy, and valence from the audio features
danceability = audio_features['danceability']
energy = audio_features['energy']
valence = audio_features['valence']

st.metric("Danceability", round(danceability, 2))
st.metric("Energy", round(energy, 2))
st.metric("Valence (Happiness)", round(valence, 2))

# --- Map of UK ---
st.subheader("🗺️ Map of UK Listening Trends")
# Example: Mapping top cities with fictional data (latitude/longitude)
uk_map = folium.Map(location=[54.5, -3], zoom_start=5)
city_coords = {
    'London': [51.5074, -0.1278],
    'Manchester': [53.4808, -2.2426],
    'Liverpool': [53.4084, -2.9916],
    'Birmingham': [52.4862, -1.8904]
}

for city, coords in city_coords.items():
    folium.CircleMarker(
        location=coords,
        radius=7,
        popup=city,
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.6
    ).add_to(uk_map)

folium_static(uk_map)

st.markdown("Data is representative and aggregated. Real-time music data is fetched directly from Spotify.")
