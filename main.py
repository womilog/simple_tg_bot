import asyncio
import os
import requests
import datetime
from aiogram import Bot, types, Dispatcher
from aiogram.enums import ParseMode.

from dotenv import find_dotenv, load_dotenv

from common.bot_cmds_list import user_private_command
from handlers.user_private import user_private_router

load_dotenv(find_dotenv())


bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
dp = Dispatcher()
dp.include_router(user_private_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=user_private_command)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
