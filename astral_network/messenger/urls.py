from django.urls import path

from messenger.views import MessageView, ChatView


urlpatterns = [
    path('chats/', MessageView.as_view(), name='messages'),
    path('chats/<int:chat_unique_code>/<int:user_id1>/<int:user_id2>/', ChatView.as_view(), name='chat'),
]