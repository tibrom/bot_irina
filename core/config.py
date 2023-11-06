import os
import datetime


from server.models import MessageType

NEW_USER_MESSAGE = 'Новый пользователь в боте.\nИмя name\nТелеграм ID tg_id'
START_MESSAGE = 'Добропожаловать, бот работает'
GREETING_ADMIN = 'Профиль успешно добавлен в администраторы'


BASE_MESSAGE = 'Новый заказ\ninfo'

SUPERVISOR_TOKEN = 'BBBB945fh7405-9g475'

DEFAULT_TOKEN = 'AAAA947hjt4398jr4ur'

BOT_TOKEN = os.getenv('BOT_TOKEN')

PREFIX = os.getenv('PREFIX')

DEFAULT_MESSAGE_TYPE_NAME =  "default"




