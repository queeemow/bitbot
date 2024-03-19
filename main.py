import telebot
import os
from dotenv.main import load_dotenv
import asyncio
from asyncio.exceptions import CancelledError
load_dotenv()

from src.bitapi import BitcoinAPI

BOT_TOKEN = os.environ['BOT_TOKEN']

class Bitcoin_price():
    BOT = None
    TASKS = {}

    def __init__(self) -> None:
        self.connect()
        @self.BOT.message_handler(content_types=["text"])
        def get_text_message_handler(message):
            return self.get_text_messages(message)

    def connect(self) -> None:
        self.BOT = telebot.TeleBot(BOT_TOKEN)

    def get_text_messages(self, message):
        asyncio.run(self.wrapper(message))

    async def wrapper(self, message):
        print("inside wrapper")
        if not message.from_user.id in self.TASKS:
            print("no user in tasks")
            self.TASKS[message.from_user.id] = asyncio.create_task(self.send_bitcoin_price(message.from_user.id))
            await self.TASKS[message.from_user.id]
        if message.text == "/unsub":
            self.delete_user(message.from_user.id)
        
    def get_bitcoin_price(self):
        price_data = BitcoinAPI.get_jsonparsed_data() 
        return str(price_data["last"])

    async def send_bitcoin_price(self, user_id) -> None:
        print("send_bit func for user " ,user_id)
        while(True):
            if not user_id in self.TASKS:
                break
            print("inside loop")
            bitcoin_price_string = self.get_bitcoin_price()
            self.BOT.send_message(user_id, "*" + bitcoin_price_string + "$*", parse_mode= 'Markdown')
            try:
                await asyncio.sleep(600)
            except CancelledError:
                print('cancel_me(): cancel sleep')
                
    def delete_user(self, user_id) -> None:
        try:
            print("unsub for user ", user_id)
            del self.TASKS[user_id]
        except:
            del self.TASKS[user_id]

    def start_polling(self):
        self.BOT.infinity_polling(timeout=100, long_polling_timeout = 100)

if __name__ == "__main__":
    bit_price = Bitcoin_price()
    bit_price.start_polling()