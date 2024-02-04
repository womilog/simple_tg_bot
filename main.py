from config import weather_api_key
from pprint import pprint
import requests
import datetime

def get_weather(city, api_key):

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
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={api_key}')
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
        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}****\n"
              f"[+]Погода в городе: {name_city}\n[+]Температура: {temperature} C°\n[+]Ощущается: {feels_like}\n[+]Описание: {description + '' + smile}\n"
              f"[+]Влажность: {humidity}%\n[+]Давление: {pressure} мм.рт.ст\n[+]Ветер: {wind} м/c\n"
              f"[+]Восход: {sunrise}\n[+]Закат: {sunset}\n[+]Продолжительность дня: {lenth_of_day}\n"
              f"Хорошего дня!!!")
    except Exception as ex:
        print(ex, "[-]Проверьте, правильное ли название города вы ввели", sep="\n")

def main():
    inp = input("[?]Введите город: ")
    get_weather(inp, weather_api_key)

if __name__ == "__main__":
    main()




