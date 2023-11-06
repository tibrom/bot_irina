import datetime
from collections import defaultdict
from sqlalchemy import select
from typing import List
from fastapi import HTTPException
from .base_repositories import BaseRepository

from bot.create_bot import bot
from core.logger import logger

from core.config import BASE_MESSAGE
from .models import MessageType
from db.data_base import users
from db.base import database



class MainRepository(BaseRepository):
    

    async def send_message(self, message: MessageType):
        query = users.select().where(
            users.c.is_supervisor==True
        )
        supervisor_info = await database.fetch_all(query)
        answer  = BASE_MESSAGE + f'\n{message.detali}\n{message.id}'
        await bot.send_message(
            message.tg_id,
            text=answer
        )
        supervisor_message = answer + f'\n Получил заявку:{message.recipient}'
        for supervisor in supervisor_info:
            await bot.send_message(
                supervisor.tg_id,
                text=supervisor_message
            )
        





