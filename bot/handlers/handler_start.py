import aiohttp
import json



from aiogram import types, Dispatcher, F
from aiogram.filters import CommandStart

from ..create_bot import bot


from db.data_base import users


from db.base import database

from core.config import NEW_USER_MESSAGE, START_MESSAGE, GREETING_ADMIN, DEFAULT_TOKEN



async def user_control(message: types.Message):
    new_user_message = NEW_USER_MESSAGE
    new_user_message.replace('name', message.from_user.username)
    new_user_message.replace('tg_id', message.from_user.id)
    query_user = users.select().where(
        users.c.tg_id==message.from_user.id,
    )
    user_info = database.fetch_one(query_user)
    if user_info is None:
        value = {
            'tg_id': message.from_user.id,
            'is_admin': False
        }
        query = users.insert().values(**value)
        await database.execute(query)
        query = users.select().where(
            users.c.is_admin==True
        )
        admin = database.fetch_all(query)
        for adm in admin:
            await bot.send_message(
                adm.tg_id,
                text=new_user_message
            )
    
    await bot.send_message(
        message.from_user.id,
        text=START_MESSAGE
    )


async def new_admin(message: types.Message):
    if message.text != DEFAULT_TOKEN:
        return
    
    query_user = users.select().where(
        users.c.tg_id==message.from_user.id,
        users.c.is_admin==True
    )
    user_info = database.fetch_one(query_user)
    if user_info is None:
        value = {
            'is_admin': True
        }
        query = users.update().where(users.tg_id==message.from_user.id).values(**value)
        await database.execute(query)
    await bot.send_message(
        message.from_user.id,
        text=GREETING_ADMIN
    )


def register_handler(dp: Dispatcher):
    dp.message.register(user_control, CommandStart())
    dp.message.register(new_admin, F.text.startswith("AAAA"))
    