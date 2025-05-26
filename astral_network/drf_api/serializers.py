from rest_framework import serializers

from auth_user.models import AuthUser
from interaction_core.models import Music, Friends
from messenger.models import Chat, Message
from profile_user.models import ProfileUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = (
            'id', 'connection_code', 'first_name',
            'last_name', 'email', 'is_active',
            'date_joined',
        )


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProfileUser
        fields = (
            'id', 'photo', 'birthdate',
            'about_yourself', 'status', 'gender',
            'user'
        )


class MusicSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Music
        fields = (
            'id', 'author', 'title',
            'music', 'user'
        )


class ChatSerializer(serializers.ModelSerializer):
    user1 = UserSerializer(read_only=True)
    user2 = UserSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = (
            'id', 'unique_chat_code', 'user1',
            'user2',
        )


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    chat = ChatSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'


class FriendSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    friend = UserSerializer(read_only=True)

    class Meta:
        model = Friends
        fields = (
            'user', 'friend', 'status',
            'friend_unique_code'
        )