from django.urls import path
from . import views, apps


urlpatterns = [
    path("", views.homepage, name='default'),
    path('login/', apps.login, name='login'),
    path('callback/', apps.callback, name='callback'),
]

app_name = "main"   
