import aiohttp
import json
import os
import random
from sqlalchemy import select


from aiogram import types, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import ChatMemberUpdated
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, JOIN_TRANSITION, IS_NOT_MEMBER, MEMBER
from core.config import chat_id
from core.logger import logger

from ..create_bot import bot


from db.data_base import users, chats, super_user


from db.base import database
from generate_report import make_request_and_send

from core.config import NEW_CHAT_MESSAGE, START_MESSAGE, GREETING_ADMIN, DEFAULT_TOKEN, DELETE_CHAT_MESSAGE

CHAT_ID = os.getenv("CHAT_ID")

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
    query = users.select().join(super_user).where(
        users.c.tg_id==str(message.from_user.id)
    )
    admin = await database.fetch_one(query)
    if admin is not None:
        logger.info(f'chat_id {chat_id}')
        await make_request_and_send(chat_id)
    else:
        await bot.send_message(
            chat_id,
            text='Функционал доступен только для супер пользователей'
        )

CHARS = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

def get_random_code() ->str:
    password = ''
    for n in range(12):
        password += random.choice(CHARS)
    
    return password

async def create_superUser(message: types.Message):
    query = users.select().where(
        users.c.tg_id==str(message.from_user.id)
    )
    admin = await database.fetch_one(query)
    if admin is not None and admin.is_admin == True:
        code = "SUPER" + get_random_code()
        value = {
            'key': code
        }
        query = super_user.insert().values(**value)
        await database.execute(query)
        await message.answer(
            code
        )

async def add_superUser(message: types.Message):
    code = message.text
    query = users.select().where(
        users.c.tg_id==str(message.from_user.id)
    )
    user = await database.fetch_one(query)
    if user is None:
        logger.error(f'Нет такого пользователя')
        return
    query = super_user.select().where(
        super_user.c.key==code
    )
    answer = await database.fetch_one(query)
    if answer is not None and answer.name is None:
        value = {
            'name':message.from_user.first_name,
            'user_id':user.id 
        }
        query = super_user.update().where(super_user.c.id==answer.id).values(**value)
        await database.execute(query)
        await message.answer("Аккаунт в супер пользователи")
    logger.error(f'Нет такого кода')


async def get_superUser(message: types.Message):
    query = users.select().where(
        users.c.tg_id==str(message.from_user.id)
    )
    admin = await database.fetch_one(query)
    if admin is not None and admin.is_admin == True:
        text = 'Список супер пользователей\n'
        query2 = super_user.select()
        answer = await database.fetch_all(query2)
        for user in answer:
            text += f"Имя пользователя {user.name} код {user.key} \n"
        text += 'для удаления пользователя отправьте "удалить-код"\n Например: "удалить-SUPER49ар59ар57ке"'
        await bot.send_message(
            message.from_user.id,
            text=text
        )

async def delete_superUser(message: types.Message):
    query = users.select().where(
        users.c.tg_id==str(message.from_user.id)
    )
    admin = await database.fetch_one(query)
    if admin is not None and admin.is_admin == True:
        data = message.text.split('-')
        query = super_user.select().where(
            super_user.c.key==data[1]
        )
        answer = await database.fetch_one(query)
        if answer is not None:
            query = super_user.delete().where(
                super_user.c.id==answer.id
            )
            await database.execute(query)
            await bot.send_message(
                message.from_user.id,
                text='Супер пользователь удален'
            )
    await bot.send_message(
        message.from_user.id,
        text='Не удалось удалить супер пользователя, попробуйте еще раз в сообщении не должно быть пробелов и лишних символов'
    )




def register_handler(dp: Dispatcher):
    dp.message.register(user_control, CommandStart())
    dp.message.register(new_admin, F.text.startswith("AAAA"))
    dp.message.register(add_superUser, F.text.startswith("SUPER"))
    dp.message.register(delete_superUser, F.text.startswith("удалить-SUPER"))
    dp.message.register(get_superUser, F.text.startswith("Получить супер пользователей"))
    dp.message.register(create_superUser, F.text.startswith("Добавить супер пользователя"))
    dp.message.register(generate_report, F.text.startswith("Получить отчет"))
    dp.my_chat_member.register(on_new_chat_member, ChatMemberUpdatedFilter(
        member_status_changed=IS_NOT_MEMBER >> MEMBER
    ))
    dp.my_chat_member.register(on_left_chat_member, ChatMemberUpdatedFilter(
        member_status_changed=MEMBER >> IS_NOT_MEMBER
    ))
    