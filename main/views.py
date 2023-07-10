from django.shortcuts import redirect, render
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pygame
import random
import json
from .config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

def homepage(request):
    return render(request, 'home.html')


def login(request):
    scope = "user-read-playback-state user-modify-playback-state playlist-read-private"
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

    for playlist in playlists_dict['items']:
        id = playlist['id']
        name = playlist['name']
        image_url = playlist['images'][1]['url']
        playlists.append({'id' : id, 'name' : name, 'image_url' : image_url}) 
    
    context = {
        'header1' : 'Playlists names:',
        'playlists' : playlists
    }

    return render(request, 'result.html', context)


def get_all_tracks(request, playlist_id):
    access_token = request.session['access_token']
    sp = spotipy.Spotify(auth = access_token)

    tracks_dict = sp.playlist_tracks(playlist_id)
    tracks = []

    for track in tracks_dict['items']:
        if track['is_local'] == False:
            uri = track['track']['uri']
            name = track['track']['name']
            artist = track['track']['artists'][0]['name']
            image_url = track['track']['album']['images'][1]['url']
            tracks.append({'uri' : uri, 'name' : name, 'artist' : artist, 'image_url' : image_url}) 

    request.session['current_playlist'] = tracks

    return play_random_track(request)

def play_random_track(request):
    access_token = request.session['access_token']
    sp = spotipy.Spotify(auth = access_token)
    tracks = request.session['current_playlist']

    random_track = random.choice(tracks)
    request.session['current_track'] = random_track
    error = ''

    try:
        sp.start_playback(uris = [random_track['uri']])
    except:
        if sp.devices()['devices'] == []:
            error = 'No devices found'
            print(error)
        else: 
            device_id = sp.devices()['devices'][0]['id']
            sp.transfer_playback(device_id = device_id)
            sp.start_playback(uris = [random_track['uri']])
    else:
        sp.start_playback(uris = [random_track['uri']])

    context = {
        'error' : error,
        'track' : random_track,
    }
    return render(request, 'game.html', context)
    
def pause_track(request):
    access_token = request.session['access_token']
    sp = spotipy.Spotify(auth = access_token)
    current_track = request.session['current_track']

    sp.pause_playback()
    context = {
        'track' : current_track,
    }
    return render(request, 'game.html', context)



