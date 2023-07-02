# pip install -r requirements.txt

from django.shortcuts import render
from . import apps

def homepage(request):
    return render(request, 'home.html')


