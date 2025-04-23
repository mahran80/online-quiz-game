from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer


class ChatRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rooms = ChatRoom.objects.filter(members=request.user)
        serializer = ChatRoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        room = ChatRoom.objects.create(name=request.data['name'])
        room.members.add(request.user)
        serializer = ChatRoomSerializer(room)
        return Response(serializer.data)


class ChatMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, roomId):
        messages = ChatMessage.objects.filter(chat__roomId=roomId)
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
