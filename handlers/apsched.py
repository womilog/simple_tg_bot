from aiogram import Bot

async def send_message_end_day(bot: Bot):
    await bot.send_message(935832114, "Заканчивай день. Надевай носки, открывай окно и медитируй")

async def send_message_plans(bot: Bot):
    await bot.send_message(935832114, "Напиши подробно список дел на завтра")