import os
import telepot
from dotenv import load_dotenv

load_dotenv(override=True)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


class TelegramLogger:

    def __init__(self):
        self.bot = telepot.Bot(TELEGRAM_TOKEN)
        self.chat_id = -506545751

    def send_msg(self, txt: str):
        try:
            self.bot.sendMessage(chat_id=self.chat_id, text=txt)
        except:
            print(f'Telegram msg failed: {txt}')