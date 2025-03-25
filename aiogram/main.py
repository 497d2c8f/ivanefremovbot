import asyncio
import os
from handlers import router
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


BOT_TOKEN = os.getenv("BOT_TOKEN")


async def main():

	bot = Bot(token=BOT_TOKEN)
	dp = Dispatcher()
	dp.include_router(router)
	await dp.start_polling(bot)


if __name__ == '__main__':

	asyncio.run(main())
