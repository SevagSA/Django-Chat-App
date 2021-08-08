from django.urls import path
from .views import (home, room, PrivateRoomSelector,
                    ChatRoomListView, PrivateChatRoomListView)


app_name = 'chat'
urlpatterns = [
    path('', home, name='home'),
    path('private-room/', PrivateRoomSelector.as_view(),
         name='private_room_selector'),
    path('rooms/', ChatRoomListView.as_view(), name='char_room_list'),
    path('rooms/private/', PrivateChatRoomListView.as_view(),
         name='private_room_list'),
    path('rooms/<str:room_name>/', room, name='room')
]
