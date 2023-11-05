from databases import Database
from sqlalchemy import create_engine, MetaData
import os




DATABASE_URL = "postgresql://root:root@bot_db_irina:5432/bot_data_irina" #os.getenv('DATABASE_URL')

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(
    DATABASE_URL,
)