from django.urls import path

from drf_api.views import UserListAPIView, ChatListAPIView


urlpatterns = [
    path('api/v1/list-users/', UserListAPIView.as_view()),
    path('api/v1/list-chats/', ChatListAPIView.as_view()),
]