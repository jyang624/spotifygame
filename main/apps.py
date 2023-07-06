from django.apps import AppConfig
from django.shortcuts import redirect, render
import os
import sys
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pygame
from .config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
import json

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
    token_dict = sp_oauth.get_access_token(code, check_cache=False)
    access_token = token_dict['access_token']
    request.session['access_token'] = access_token
    return render(request, 'result.html', token_dict)


def get_user_playlists(request):
    access_token = request.session['access_token']
    sp = spotipy.Spotify(auth = access_token)

    playlists_dict = sp.current_user_playlists()
    playlists = []

    for i in range(len(playlists_dict['items'])):
        name = playlists_dict['items'][i]['name']
        url = playlists_dict['items'][i]['images'][1]['url']
        playlists.append({'playlists_names' : name, 'playlists_image_urls' : url}) 
    
    context = {
        'header1' : 'Playlists names:',
        'access_token' : access_token,
        'playlists' : playlists
    }
    # print(json.dumps(playlists_dict['items'],sort_keys=False,indent=4))
    return render(request, 'result.html', context)


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