from dotenv import load_dotenv
import os
import requests
from datetime import datetime

# COLORS 
RESET = '\033[0m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
BLUE = '\033[94m'

# ICONS
ICONS = {
    'Clear': '☀️',
    'Clouds': '☁️',
    'Rain': '🌧️',
    'Drizzle': '🌦️',
    'Thunderstorm': '⛈️',
    'Snow': '🌨️',
    'Mist': '🌫️',
    'Fog': '🌫️',
    'Haze': '🌫️',
    'Smoke': '🌫️',
    'Dust': '🌫️',
    'Sand': '🌫️',
    'Ash': '🌋',
    'Squall': '🌬️',
    'Tornado': '🌪️'
}

# API
load_dotenv()
API_KEY = os.getenv('YOUR_API_KEY')
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

# FUNCTIONS
    
def get_advice(temp, weather_main, wind):
    if weather_main in ['Rain', 'Drizzle']:
        return 'Weź parasol - będzie mokro.'
    if weather_main == 'Snow':
        return 'Pada śnieg - ubierz się ciepło i uważaj na drodze.'
    if weather_main == 'Thunderstorm':
        return 'Uwaga! Burza - lepiej zostań w domu.'
    if weather_main in ['Mist', 'Fog', 'Haze']:
        return 'Jest mgliście - zachowaj ostrożność.'
    
    if temp < 0:
        return 'Bardzo zimno - koniecznie załóż czapkę i rękawiczki.'
    if temp < 10:
        return 'Chłodno - przyda się kurtka.'
    if temp > 25:
        return 'Gorąco - pij dużo wody.'
    if temp > 30:
        return 'Upał - unikaj słońca w południe.'
    
    if wind > 10:
        return 'Wieje mocny wiatr - uważaj.'
    
    return 'Pogoda wygląda całkiem w porządku.'

def color_temp(temp):
    if temp <0:
        return '\033[94m'
    if temp <10:
        return '\033[96m'
    if temp <20:
        return '\033[93m'
    if temp <30:
        return '\033[92m'
    return '033[91m'

def save_to_file(city, temp, desc, icon, advice):
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    line = f'{now} | {city} | {temp}°C | {desc} | {icon} | {advice}\n'
    with open('weather_log.txt', 'a', encoding='utf-8') as f:
              f.write(line)

# INPUT
city = input('Podaj miasto: ')
print('Wpisałeś: ', city)
    
# PARAMS
params = {
    'q': city,
    'appid': API_KEY,
    'units': 'metric',
    'lang': 'pl'
}

# API REQUEST
try:
    response = requests.get(BASE_URL, params=params)
except requests.exceptions.RequestException:
    print('Błąd: brak połączenia z internetem lub problem z API.')

# API ERRORS
if response.status_code != 200:
    print('Błąd: API zwróciło kod', response.status_code)
    exit()

# DICTIONARY
data = response.json()

temp = data['main']['temp']
desc = data['weather'][0]['description']
humidity = data['main']['humidity']
wind = data['wind']['speed']

weather_main = data['weather'][0]['main']
icon = ICONS.get(weather_main, '❓')

temp_color = color_temp(temp)

# OUTPUT
print(f'\n{CYAN}--- Pogoda dla: {city} ---{RESET}')
print(f'{icon}  {YELLOW}Temperatura:{RESET} {temp_color}{temp} °C{RESET}')
print(f'{GREEN}Opis:{RESET} {desc}')
print(f'{BLUE}Wilgotność:{RESET} {humidity} %')
print(f'{CYAN}Prędkość wiatru:{RESET}', wind, 'm/s')

advice = get_advice(temp, weather_main, wind)
print(f'\nPorada: {advice}')

save_to_file(city, temp, desc, icon, advice)
print('Zapisano do pliku: weather_log.txt')