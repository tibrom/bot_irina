import os
import datetime

from db.data_base import message_types
from server.models import MessageType

NEW_USER_MESSAGE = 'Новый пользователь в боте.\nИмя name\nТелеграм ID tg_id'
START_MESSAGE = 'Добропожаловать, бот работает'
GREETING_ADMIN = 'Профиль успешно добавлен в администраторы'


BASE_MESSAGE = 'Новый заказ\ninfo'


DEFAULT_TOKEN = 'AAAA947hjt4398jr4ur'

BOT_TOKEN = os.getenv('BOT_TOKEN')

PREFIX = os.getenv('PREFIX')

DEFAULT_MESSAGE_TYPE_NAME =  "default"




