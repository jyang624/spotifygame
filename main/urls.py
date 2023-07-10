from django.urls import path
from . import views


urlpatterns = [
    path("", views.homepage, name='default'),
    path('login/', views.login, name='login'),
    path('callback/', views.callback, name='callback'),
    path('get_user_playlists/', views.get_user_playlists, name='get_user_playlists'),
    path('get_all_tracks/<str:playlist_id>', views.get_all_tracks, name='get_all_tracks'),
    path('play_random_track/', views.play_random_track, name='play_random_track'),
    path('pause_track/', views.pause_track, name='pause_track'),
]

app_name = "main"   
