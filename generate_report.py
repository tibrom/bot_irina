import os
import asyncio
import logging
from datetime import datetime, timedelta
import json

from aiogram import Bot, Dispatcher, types

import aiohttp

# Ваш токен бота от BotFather
TOKEN = os.getenv("BOT_TOKEN")
# ID чата, куда будут отправляться данные
CHAT_ID = os.getenv("CHAT_ID")



bot = Bot(token=TOKEN)

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage








bot = Bot(TOKEN, parse_mode=ParseMode.HTML)





async def get_text(url, city):
    text_result = ''
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = {}
            code = response.status
            print(code)
            dt = await response.text()
            if dt == "Remote is not active or does not exist":
                return
            print(dt)
            ds = json.loads(dt)
            data = json.loads(ds)
            
            
            
            print(data)
            if data.get('percent') is not None:
                print(data.get('percent'))
                if float(data.get('percent')) >= float(data.get('plan')):
                    flag = "✔️"
                else:
                    flag = "❌"
                text = f"{city} -- {data.get('summ')}--{data.get('meetings')}/{data.get('meetings_sales')}--{data.get('percent')}% {flag}"
                return text
                
    
        return text_result


async def make_request_and_send(chat_id):
    kb = [
        [
            types.KeyboardButton(text="Получить отчет"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Обновленные данные"
    )

    url = 'http://vesnarsc.ru/Remotes/hh65rfsdcjoiH58dfv54t8c8x5wGGG147Flloc'
    async with aiohttp.ClientSession() as session:
        text = ''
        async with session.get(url) as response:
            dt = await response.text()
            print(dt)
            data_list = json.loads(dt)
            for dt_entry in data_list:
                print(dt_entry)
                if dt_entry.get("gorod") is not None:
                    print(dt_entry.get("gorod"))
                    try:
                        message_text = await get_text(
                            url=f"http://vesnarsc.ru/Remotes/{dt_entry.get('name')}",
                            city=dt_entry.get("gorod")
                        )
                        text += message_text + "\n"
                    except: pass
            await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)



    # Отправляем данные в чат
    


async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        print(current_time)

        # Планируем запрос только в указанные часы
        if current_time in ["14:00", "17:00", "19:00", "21:00"]:
            await make_request_and_send(chat_id=CHAT_ID)

if __name__ == '__main__':
    asyncio.run(scheduled(60))