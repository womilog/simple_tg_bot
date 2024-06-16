from datetime import datetime
import requests
from bs4 import BeautifulSoup

tracks_dict = {
    'Заветы-Ильича--Ярославский Вокзал': 'zavety-ilicha--moskva-yaroslavskaya',
    'Ярославский Вокзал--Заветы-Ильича': 'moskva-yaroslavskaya--zavety-ilicha',
    'Заветы-Ильича--Пушкино': 'zavety-ilicha--pushkino,moskovskaya-obl',
    'Пушкино--Заветы-Ильича': 'pushkino,moskovskaya-obl--zavety-ilicha',
}

def get_trips(track):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    date = datetime.now().strftime("%d-%m-%Y").replace('-', '.')
    hour = float(datetime.now().strftime("%H-%M").replace('-', '.'))
    response = requests.get(f"https://poezdato.net/raspisanie-poezdov/{tracks_dict[track]}/{date}/", headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    times_trips = soup.find_all('span', class_="_time")
    all_trips = [(float(times_trips[i].text), float(times_trips[i+1].text)) for i in range(0, len(times_trips), 2)]
    current_trips = [f"[+] Отправление: {str(x[0])}  ➡️  " + f"Прибытие: {str(x[1])}" for x in all_trips if x[0] > hour][:5]
    return '\n'.join(current_trips)





get_trips('Заветы-Ильича--Ярославский Вокзал')


