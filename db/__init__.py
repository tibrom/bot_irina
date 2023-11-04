from .base import metadata, engine, DATABASE_URL

from .data_base import message_types, message_type_chats, chats




metadata.create_all(bind=engine)