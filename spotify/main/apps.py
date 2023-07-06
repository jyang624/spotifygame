from django.apps import AppConfig
from django.shortcuts import redirect, render
import os
import sys
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pygame
from .config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
from django.http import HttpResponse

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

def login(request):
    scope = "user-modify-playback-state playlist-read-private"
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope)
    redirect_url = sp_oauth.get_authorize_url()
    return redirect(redirect_url)

def callback(request):
    scope = "user-modify-playback-state playlist-read-private"
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope)
    code = request.GET.get('code')
    token = sp_oauth.get_access_token(code, check_cache=False)
    request.session['token'] = token
    return render(request, 'result.html', token)

# Does not work
def logout():
    scope = "user-modify-playback-state playlist-read-private"
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope)
    cached_token = sp_oauth.get_cached_token()
    if cached_token:
        sp_oauth.cache_handler.remove_cached_token()()
        return "User logged out successfully"
    else:
        return "No cached token found"

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