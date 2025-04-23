from django.urls import path
from .views import ChatRoomView, ChatMessagesView

urlpatterns = [
    path('rooms/', ChatRoomView.as_view(), name='chat_rooms'),
    path('rooms/<str:roomId>/messages/', ChatMessagesView.as_view(), name='chat_messages'),
]
