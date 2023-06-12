import os
import sys
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pygame

# Get the Spotify client ID and secret from environment variables
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

# Authenticate with Spotify
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_user_playlists(username):
    user_playlists = []
    results = spotify.current_user_saved_playlists(username)
    for item in results['playlists']['items']:
        user_playlists.append(item['playlist']['name'])
    return user_playlists

def get_random_track_from_playlist(playlist_name, track_name):
    user_playlists = get_user_playlists(username)
    selected_playlist = random.choice(user_playlists)
    track_name = random.choice(spotify.playlist_tracks(selected_playlist, track_name))
    return track_name

def play_track(track_name):
    track_url = spotify.playlist_tracks(get_user_playlists(username), track_name)[0]['track']['track']['uri']
    pygame.mixer.music.load(track_url)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass


