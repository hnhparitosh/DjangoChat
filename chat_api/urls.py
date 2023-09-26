from django.urls import path
from .views import UserRegistrationView, UserLoginView, get_online_users, StartChatView, send_message

urlpatterns = [
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/login/', UserLoginView.as_view(), name='login'),
    path('api/online-users/', get_online_users, name='online-users'),
    path('api/chat/start/', StartChatView.as_view(), name='start-chat'),
    path('api/chat/send/', send_message, name='send-message'),
]
