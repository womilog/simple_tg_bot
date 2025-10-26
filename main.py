import asyncio
import os
from datetime import datetime, timezone, timedelta
from sched import scheduler
from shlex import shlex

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers import apsched
from middleware.apschedulermiddleware import SchedulerMiddleware

from dotenv import find_dotenv, load_dotenv

from common.bot_cmds_list import user_private_command
from handlers.user_private import user_private_router

load_dotenv(find_dotenv())


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
dp.include_router(user_private_router)

current_date = datetime.now().date()
end_day_datetime = datetime(
    year=current_date.year,
    month=current_date.month,
    day=current_date.day,
    hour=22,
    minute=30,
    second=0
)
plans_datetime = datetime(
    year=current_date.year,
    month=current_date.month,
    day=current_date.day,
    hour=22,
    minute=20,
    second=0
)

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
scheduler.add_job(apsched.send_message_end_day, trigger='cron', hour=end_day_datetime.hour,
                  minute=end_day_datetime.minute, start_date=datetime.now(), kwargs={'bot': bot})
scheduler.add_job(apsched.send_message_end_day, trigger='cron', hour=plans_datetime.hour,
                  minute=plans_datetime.minute, start_date=datetime.now(), kwargs={'bot': bot})
dp.update.register((SchedulerMiddleware(scheduler)))

async def main():
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=user_private_command)
    print('Бот запущен')
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
