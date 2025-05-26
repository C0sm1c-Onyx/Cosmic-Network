import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser

from messenger.models import Chat, Message
from profile_user.models import ProfileUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.chat_code = self.scope['url_route']['kwargs']['unique_chat_code']
            self.chat_group_name = f"chat_{self.chat_code}"

            if isinstance(self.scope['user'], AnonymousUser):
                await self.close()
                return

            if not await self.check_chat_access():
                await self.close()
                return

            await self.channel_layer.group_add(
                self.chat_group_name,
                self.channel_name
            )
            await self.accept()

            await self.send_chat_history()
            
        except Exception as e:
            print(f"Error in connect: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.chat_group_name,
                self.channel_name
            )
        except Exception as e:
            print(f"Error in disconnect: {str(e)}")

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            user = self.scope['user']

            if not message.strip():
                return

            await self.save_message(user, message, self.chat_code)

            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    'type': 'chat.message',
                    'message': message,
                    'user': {
                        'id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'profile': await self.get_profile_user(user.id)
                    },
                }
            )
        except Exception as e:
            print(f"Error in receive: {str(e)}")

    async def chat_message(self, event):
        try:
            message = event['message']
            user = event['user']

            await self.send(text_data=json.dumps({
                'message': message,
                'user': user
            }))
        except Exception as e:
            print(f"Error in chat_message: {str(e)}")

    @database_sync_to_async
    def check_chat_access(self):
        try:
            chat = Chat.objects.get(unique_chat_code=self.chat_code)
            return chat.user1 == self.scope['user'] or chat.user2 == self.scope['user']
        except Chat.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, user, message, chat_code):
        try:
            chat = Chat.objects.get(unique_chat_code=chat_code)
            message = Message.objects.create(
                sender=user,
                message=message,
                chat=chat
            )
            message.save()
            return message
        except Exception as e:
            print(f"Error saving message: {str(e)}")
            return None

    @database_sync_to_async
    def get_chat_history(self):
        try:
            chat = Chat.objects.get(unique_chat_code=self.chat_code)
            messages = Message.objects.filter(chat=chat).order_by('sending_time')[:100]
            print()
            return [{
                'message': msg.message,
                'user': {
                    'id': msg.sender.id,
                    'first_name': msg.sender.first_name,
                    'last_name': msg.sender.last_name,
                    'profile': ProfileUser.objects.get(user=msg.sender.id).photo.url
                },
            } for msg in messages]
        except Exception as e:
            print(f"Error getting chat history: {str(e)}")
            return []

    @database_sync_to_async
    def get_profile_user(self, id):
        return ProfileUser.objects.get(user=id).photo.url

    async def send_chat_history(self):
        try:
            history = await self.get_chat_history()
            await self.send(text_data=json.dumps({
                'type': 'chat.history',
                'messages': history
            }))
        except Exception as e:
            print(f"Error sending chat history: {str(e)}")
