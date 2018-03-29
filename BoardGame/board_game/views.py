from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

def index(request):
    return render(request, 'board_game/index.html', {})

def room(request, room_name):
    return render(request, 'board_game/room.html', {})
