from .base import metadata, engine, DATABASE_URL

from .data_base import users




metadata.create_all(bind=engine)