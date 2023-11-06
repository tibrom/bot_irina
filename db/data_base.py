import datetime
from sqlalchemy import Table, Column, String, Boolean, Integer, DateTime, ForeignKey

from .base import metadata


users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, unique= True),
    Column('created_at', DateTime, default=datetime.datetime.utcnow()),
    Column('tg_id', String),
    Column('is_admin', Boolean)
)


chats = Table(
    'chats',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, unique= True),
    Column('tg_chat_id', String),
    Column('name', String),
)
