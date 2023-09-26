from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Chat, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id',)

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'chat', 'sender', 'content', 'timestamp')
