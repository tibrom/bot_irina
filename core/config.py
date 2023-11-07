import os
import datetime


from server.models import MessageType

NEW_CHAT_MESSAGE = 'Бот добавлен в новую группу.\nГруппа: name\nID: tg_id'
DELETE_CHAT_MESSAGE = 'Бот удален из группы.\nГруппа: name\nID: tg_id'
START_MESSAGE = 'Добропожаловать, бот работает'
GREETING_ADMIN = 'Профиль успешно добавлен в администраторы'


BASE_MESSAGE = 'Новая заявка'



DEFAULT_TOKEN = 'AAAA947hjt4398jr4ur'

BOT_TOKEN = os.getenv('BOT_TOKEN')

PREFIX = os.getenv('PREFIX')

DEFAULT_MESSAGE_TYPE_NAME =  "default"




