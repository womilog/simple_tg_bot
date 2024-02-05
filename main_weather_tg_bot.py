import requests
import datetime
# from config import weather_api_key, tg_bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram import executor

weather_api_key = "4b1ba4a5df282e1523b183ee6c11ab65"
tg_bot_token = "6758413307:AAHagVHKLTgoqH42nECVFyTqr4rij1njYgM"
bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("[?]Привет! Напиши мне название своего города")

@dp.message_handler()
async def get_weather(message: types.Message):

    dict_smiles = {
        "Clear": "\U00002600",
        "Clouds": "\U00002601",
        "Rain": "\U00002614",
        "Drizzle": "\U00002614",
        "Thunderstorm": "\U000026A1",
        "Show": "\U0001F328",
        "Mist": "\U0001F32B"
    }

    try:
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&units=metric&lang=ru&appid={weather_api_key}')
        data = response.json()
        #pprint(data)
        name_city = data["name"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        wind = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        lenth_of_day = (datetime.datetime.fromtimestamp(data["sys"]["sunset"]) -
                        datetime.datetime.fromtimestamp(data["sys"]["sunrise"]))
        main_key = data["weather"][0]["main"]
        smile = dict_smiles[main_key] if main_key in dict_smiles else ""
        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}****\n"
              f"[+]Погода в городе: {name_city}\n[+]Температура: {temperature} C°\n[+]Ощущается: {feels_like}\n[+]Описание: {description + '' + smile}\n"
              f"[+]Влажность: {humidity}%\n[+]Давление: {pressure} мм.рт.ст\n[+]Ветер: {wind} м/c\n"
              f"[+]Восход: {sunrise}\n[+]Закат: {sunset}\n[+]Продолжительность дня: {lenth_of_day}\n"
              f"***Хорошего дня!!!***")
    except Exception as ex:
        await message.reply(ex, "[-]Проверьте, правильное ли название города вы ввели", sep="\n")


if __name__ == "__main__":
    executor.start_polling(dp)
