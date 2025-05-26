from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

from drf_api.serializers import ProfileSerializer, ChatSerializer, MessageSerializer
from auth_user.models import AuthUser
from profile_user.models import ProfileUser
from messenger.models import Chat, Message


class BaseListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    model_class = None
    serializer_class = None
    return_data_name = None

    @method_decorator(ratelimit(key='ip', rate='10/m', method='GET'))
    def get(self, request, *args, **kwargs):
        data = self.serializer_class(self.get_queryset(), many=True).data
        return Response({self.return_data_name: data})

    def get_queryset(self):
        return self.model_class.objects.all()


class UserListAPIView(BaseListAPIView):
    model_class = ProfileUser
    serializer_class = ProfileSerializer
    return_data_name = 'users'


class ChatListAPIView(BaseListAPIView):
    model_class = Message
    serializer_class = MessageSerializer
    return_data_name = 'messages'
