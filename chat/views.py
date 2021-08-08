import json

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import ChatRoom
from .forms import PrivateChatSelectorForm, MessageForm


def home(request):
    return render(request, 'chat/home.html')


@login_required
def room(request, room_name):
    # TODO replace with CBV if possible
    try:
        room = ChatRoom.objects.get(room_name=room_name)
        if room.is_private and request.user not in room.users.all():
            messages.error(request, "You are not allowed in this room")
            return redirect(reverse('chat:home'))
    except ChatRoom.DoesNotExist:
        pass

    form = MessageForm(request.user, room)
    if request.method == 'POST':
        form = MessageForm(request.user, room,
                           request.POST, request.FILES)
        if form.is_valid():
            form.save()

    return render(request, 'chat/room.html', {'form': form, 'room_name': room_name})


class PrivateRoomSelector(CreateView, LoginRequiredMixin):
    model = ChatRoom
    form_class = PrivateChatSelectorForm
    template_name = 'chat/private_room_selector.html'

    def get_form_kwargs(self):
        kwargs = super(PrivateRoomSelector, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        room_name = self.request.POST.get('room_name')
        return reverse_lazy('chat:room', kwargs={'room_name': room_name})


class ChatRoomListView(ListView, LoginRequiredMixin):
    model = ChatRoom
    queryset = ChatRoom.objects.filter(is_private=False)
    context_object_name = 'rooms'


class PrivateChatRoomListView(ListView, LoginRequiredMixin):
    model = ChatRoom
    context_object_name = 'rooms'

    def get_queryset(self):
        queryset = ChatRoom.objects.filter(
            users__in=[self.request.user], is_private=True)
        return queryset
