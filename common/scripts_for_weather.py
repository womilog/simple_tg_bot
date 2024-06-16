import datetime
import os
from pprint import pprint

import requests

from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())
dict_weather_smiles = {
        "Clear": "\U00002600",
        "Clouds": "\U00002601",
        "Rain": "\U00002614",
        "Drizzle": "\U00002614",
        "Thunderstorm": "\U000026A1",
        "Show": "\U0001F328",
        "Mist": "\U0001F32B"
    }


def get_weather(city):
        current_response = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={os.getenv("WEATHER")}'
        )
        current_response_data = current_response.json()
        name_city = current_response_data["name"]
        feels_like = current_response_data["main"]["feels_like"]
        humidity = current_response_data["main"]["humidity"]
        pressure = current_response_data["main"]["pressure"]
        temperature = current_response_data["main"]["temp"]
        current_description = current_response_data["weather"][0]["description"]
        wind = current_response_data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(current_response_data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(current_response_data["sys"]["sunset"])
        length_of_day = (datetime.datetime.fromtimestamp(current_response_data["sys"]["sunset"]) -
                        datetime.datetime.fromtimestamp(current_response_data["sys"]["sunrise"]))
        main_key = current_response_data["weather"][0]["main"]
        smile = dict_weather_smiles[main_key] if main_key in dict_weather_smiles else ""
        current_data = (f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} 📆****\n" +
                        f"[+] Текущая погода в городе: {name_city} 🏙\n" +
                        f"[+] Температура: {temperature} C° 🤒\n" +
                        f"[+] Ощущается: {feels_like}\n" +
                        f"[+] Описание: {current_description + '' + smile}\n" +
                        f"[+] Ощущается: {feels_like} ⛄️\n" +
                        f"[+] Описание: {current_description + '' + smile}\n" +
                        f"[+] Влажность: {humidity}% 💧\n[+]Давление: {pressure} мм.рт.ст 🏋️‍♀️\n" +
                        f"[+] Ветер: {wind} м/c 💨\n" +
                        f"[+] Восход: {sunrise} 🌝\n" +
                        f"[+] Закат: {sunset} 🌚 \n" +
                        f"[+] Продолжительность дня: {length_of_day} 🌞\n")

        daily_response = requests.get(
                f'https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&lang=ru&appid={os.getenv("WEATHER")}'
        )
        daily_response_data = daily_response.json()
        data_of_day = []
        for i in range(1, 9):
                time_period = datetime.datetime.fromtimestamp(daily_response_data['list'][i]['dt'], tz=datetime.timezone.utc)
                temperature = daily_response_data['list'][i]['main']['temp']
                description = daily_response_data['list'][i]['weather'][0]['description']
                main_key = daily_response_data['list'][i]['weather'][0]['main']
                smile = dict_weather_smiles[main_key] if main_key in dict_weather_smiles else ""
                data_of_day.append(f'[+] Время: {time_period}⏳, температура: {temperature} C°, Описание: {description} {smile}')

        daily_data = 'Температура и описание в течении дня\n' + '\n'.join(data_of_day) + '\n' + '***Хорошего дня!***'
        return current_data + daily_data

