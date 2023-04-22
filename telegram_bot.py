import telegram
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
tg_api_key = os.getenv('TG_API_KEY')
chat_id = os.getenv('TG_CHAT_ID')
bot = telegram.Bot(token=tg_api_key)
print(bot.getMe())
bot.sendMessage(chat_id=chat_id, text = 'Проверка связи')
