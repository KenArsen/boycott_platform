import json
import logging
import uuid

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

# from .ai_response import get_ai_response

logger = logging.getLogger(__name__)


class AIChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_authenticated:
            self.room_group_name = f"chat_user_{user.id}"
        else:
            # Генерация уникального ID для анонимного пользователя
            anon_id = self.scope["session"].get("anon_id")
            if not anon_id:
                anon_id = str(uuid.uuid4())
                self.scope["session"]["anon_id"] = anon_id
                await database_sync_to_async(self.scope["session"].save)()
            self.room_group_name = f"chat_anon_{anon_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.send(text_data=json.dumps({"message": "Привет! Я AI-ассистент. Чем могу помочь?", "sender": "AI"}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]

            logger.info(f"Сообщение от пользователя: {message}")

            # Отправка пользовательского сообщения в группу
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": "Вы",
                },
            )

            # Отправка индикатора "AI печатает..." перед обработкой ответа
            await self.send(text_data=json.dumps({"message": "AI печатает...", "sender": "System"}))

            # Получение ответа от AI
            ai_response = await self._get_ai_response(message)

            # Отправка ответа AI
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": ai_response,
                    "sender": "AI",
                },
            )
        except Exception as e:
            logger.error(f"Ошибка в receive: {e}")
            await self.send(text_data=json.dumps({"message": f"Ошибка: {str(e)}", "sender": "System"}))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"], "sender": event.get("sender", "unknown")}))

    async def _get_ai_response(self, message):
        try:
            pass
            # return await get_ai_response(message)
        except Exception as e:
            logger.error(f"Ошибка при вызове AI: {e}")
            return "Произошла ошибка при обращении к AI. Пожалуйста, попробуйте позже."
