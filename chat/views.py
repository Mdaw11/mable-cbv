from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Room, Chat

@login_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'chat/rooms.html', {'rooms': rooms})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Chat.objects.filter(room=room)[0:25]

    return render(request, 'chat/chatroom.html', {'room': room, 'messages': messages})