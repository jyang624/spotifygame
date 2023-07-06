from django.urls import path
from . import views, apps


urlpatterns = [
    path("", views.homepage, name='default'),
    path('login/', apps.login, name='login'),
    path('callback/', apps.callback, name='callback'),
    path('get_user_playlists/', apps.get_user_playlists, name='get_user_playlists')
]

app_name = "main"   
