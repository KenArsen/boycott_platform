import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .ask import get_ai_response


class AIChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"].get("room_name", "default")
        self.room_group_name = f"chat_{self.room_name}"

        # Присоединиться к группе
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # Отправляем приветственное сообщение от AI
        await self.send(
            text_data=json.dumps({"message": "Привет! Я AI-ассистент. Чем я могу помочь вам сегодня?", "sender": "AI"})
        )

    async def disconnect(self, close_code):
        # Покинуть группу
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Получение сообщения от WebSocket
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]
            user_id = self.scope.get("user").id if not self.scope.get("user").is_anonymous else "anon"

            # Отправляем сообщение пользователя в группу
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat_message", "message": message, "sender": f"user_{user_id}"}
            )

            # Получаем ответ от AI
            ai_response = await self.get_ai_response(message)

            # Отправляем ответ AI в группу
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat_message", "message": ai_response, "sender": "AI"}
            )
        except Exception as e:
            # Обработка ошибок
            await self.send(text_data=json.dumps({"message": f"Произошла ошибка: {str(e)}", "sender": "system"}))

    # Получение сообщения из группы
    async def chat_message(self, event):
        message = event["message"]
        sender = event.get("sender", "unknown")

        # Отправка сообщения в WebSocket
        await self.send(text_data=json.dumps({"message": message, "sender": sender}))

    @database_sync_to_async
    def get_ai_response(self, message):
        # Вызываем сервис AI (может быть синхронным)
        return get_ai_response(message)
