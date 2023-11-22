import aiohttp
import json



from aiogram import types, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import ChatMemberUpdated
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, JOIN_TRANSITION, IS_NOT_MEMBER, MEMBER

from ..create_bot import bot


from db.data_base import users, chats


from db.base import database
from generate_report import make_request_and_send

from core.config import NEW_CHAT_MESSAGE, START_MESSAGE, GREETING_ADMIN, DEFAULT_TOKEN, DELETE_CHAT_MESSAGE



async def user_control(message: types.Message):
    query_user = users.select().where(
        users.c.tg_id==str(message.from_user.id),
    )
    user_info = await database.fetch_one(query_user)
    if user_info is None:
        value = {
            'tg_id': str(message.from_user.id),
            'is_admin': False,
        }
        query = users.insert().values(**value)
        await database.execute(query)
    
    await bot.send_message(
        message.from_user.id,
        text=START_MESSAGE
    )


async def new_admin(message: types.Message):
    if message.text != DEFAULT_TOKEN:
        return
    
    query_user = users.select().where(
        users.c.tg_id==str(message.from_user.id),
        users.c.is_admin==True
    )
    user_info = await database.fetch_one(query_user)
    if user_info is None:
        value = {
            'is_admin': True
        }
        query = users.update().where(users.c.tg_id==str(message.from_user.id)).values(**value)
        await database.execute(query)
    await bot.send_message(
        message.from_user.id,
        text=GREETING_ADMIN
    )

async def on_new_chat_member(event: ChatMemberUpdated):
    
    chat_id = event.chat.id
    chat_title = event.chat.title
    new_chat_message = NEW_CHAT_MESSAGE.replace('name', chat_title).replace('tg_id', str(chat_id))
    search_query =  chats.select().where(
        chats.c.tg_chat_id == str(chat_id)
    )
    ansewr = await database.fetch_one(search_query)
    if ansewr is None:
        value = {
            'tg_chat_id': str(chat_id),
            'name': str(chat_title)
        }
        query = chats.insert().values(**value)
        await database.execute(query)
        query = users.select().where(
            users.c.is_admin==True
        )
        admin = await database.fetch_all(query)
        for adm in admin:
            await bot.send_message(
                adm.tg_id,
                text=new_chat_message
            )


async def on_left_chat_member(event: ChatMemberUpdated):
    chat_id = event.chat.id
    chat_title = event.chat.title

    dalete_chat_message = DELETE_CHAT_MESSAGE.replace('name', chat_title).replace('tg_id', str(chat_id))
    search_query =  chats.select().where(
        chats.c.tg_chat_id == str(chat_id)
    )
    ansewr = await database.fetch_all(search_query)
    for chat in ansewr:
        query = chats.delete().where(
            chats.c.id==chat.id
        )
        await database.execute(query)
    query = users.select().where(
        users.c.is_admin==True
    )
    admin = await database.fetch_all(query)
    for adm in admin:
        await bot.send_message(
            adm.tg_id,
            text=dalete_chat_message
        )


async def generate_report(message: types.Message):
    await make_request_and_send()


def register_handler(dp: Dispatcher):
    dp.message.register(user_control, CommandStart())
    dp.message.register(new_admin, F.text.startswith("AAAA"))
    dp.message.register(generate_report, F.text.startswith("Получить отчет"))
    dp.my_chat_member.register(on_new_chat_member, ChatMemberUpdatedFilter(
        member_status_changed=IS_NOT_MEMBER >> MEMBER
    ))
    dp.my_chat_member.register(on_left_chat_member, ChatMemberUpdatedFilter(
        member_status_changed=MEMBER >> IS_NOT_MEMBER
    ))
    