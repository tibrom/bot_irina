from sqlalchemy import Column, Boolean
from .logger import logger



async def column_control(database, table_name, columname, type):
   
    query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' AND column_name = '{columname}'"
    result = await database .execute(query)
    exists = await result.scalar()

    if not exists:
            # Добавляем столбец
        query = f"ALTER TABLE {table_name} ADD COLUMN {columname} {type}"
        await database .execute(query)
        logger.debug(f"Столбец {columname} успешно добавлен.")
    else:
        logger.debug(f"Столбец {columname} уже существует.")