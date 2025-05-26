from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q

from auth_user.models import AuthUser
from messenger.models import Message, Chat
from profile_user.models import ProfileUser


class MessageView(View):
    def get(self, request):
        context = {
            'request_user_id': request.user.id,
            'is_auth': request.user.is_authenticated,
        }

        return render(request, 'messenger/messages.html', context)


class ChatView(View):
    def get(self, request, chat_unique_code, user_id1, user_id2):
        all_messages = Message.objects.filter(
            chat=Chat.objects.get(unique_chat_code=chat_unique_code)
        ).order_by('sending_time')

        if request.user.id == user_id1:
            profile_user1 = ProfileUser.objects.get(user=user_id1)
            profile_user2 = ProfileUser.objects.get(user=user_id2)
        else:
            profile_user1 = ProfileUser.objects.get(user=user_id2)
            profile_user2 = ProfileUser.objects.get(user=user_id1)

        context = {
            'chat_code': chat_unique_code,
            'request_user_id': request.user.id,
            'is_auth': request.user.is_authenticated,
            'all_messages': all_messages[:100],
            'profile_user1': profile_user1,
            'profile_user2': profile_user2
        }

        return render(request, 'messenger/chat.html', context)


def pre_initial_chat(request, user_id):
    try:
        current_chat = Chat.objects.get(
            Q(
                user1=request.user.id,
                user2=user_id
            )
            |
            Q(
                user1=user_id,
                user2=request.user.id
            )
        )
    except Chat.DoesNotExist:
        user1 = AuthUser.objects.get(pk=request.user.id)
        user2 = AuthUser.objects.get(pk=user_id)

        current_chat = Chat.objects.create(
            unique_chat_code=abs(
                hash(
                    int(user1.connection_code) + int(user2.connection_code)
                )
            ),
            user1=user1,
            user2=user2
        )
        current_chat.save()

    user1 = current_chat.user1
    user2 = current_chat.user2

    chat_code = current_chat.unique_chat_code
    return redirect(f'/chats/{chat_code}/{user1.id}/{user2.id}/')

