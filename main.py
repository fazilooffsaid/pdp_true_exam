import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

import handlers
import db

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_cmd(message: Message):
    await handlers.start(message)


@dp.message()
async def all_messages(message: Message):
    await handlers.handle_message(message)


async def main():
    db.init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())