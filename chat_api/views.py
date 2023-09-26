from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics, permissions
from django.db.models import Q
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Chat, Message
from .serializers import UserSerializer, ChatSerializer, MessageSerializer

# User Registration View
class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login View
class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'user_id': user.id}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Get Online Users View (You can adjust this logic based on your requirements)
@api_view(['GET'])
def get_online_users(request):
    online_users = User.objects.filter(is_online=True)
    serializer = UserSerializer(online_users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Start a Chat View
class StartChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        participants = request.data.get('participants')
        chat = Chat.objects.filter(participants__in=participants).distinct()
        if chat.exists():
            chat = chat.first()
        else:
            chat = Chat.objects.create()
            chat.participants.add(*participants)
        serializer = ChatSerializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Send a Message View
@api_view(['POST'])
def send_message(request):
    sender = request.user
    chat_id = request.data.get('chat_id')
    content = request.data.get('content')
    chat = Chat.objects.get(id=chat_id)
    if chat.participants.filter(id=sender.id).exists():
        message = Message.objects.create(chat=chat, sender=sender, content=content)
        message_serializer = MessageSerializer(message)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{chat_id}",
            {
                "type": "chat.message",
                "message": message_serializer.data
            }
        )
        return Response(message_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'You are not a participant in this chat.'}, status=status.HTTP_403_FORBIDDEN)
