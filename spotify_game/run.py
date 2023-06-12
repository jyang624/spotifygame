from app.py import get_user_playlist,

username = input("Enter your Spotify username: ")
playlist_name = input("Enter the name of the playlist from which you want to play a random track: ")
track_name = input("Enter the name of the random track to play: ")

play_track(track_name)