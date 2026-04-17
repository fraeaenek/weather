from fastapi import FastAPI
import os
from dotenv import load_dotenv
import requests
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI()

API_KEY = os.getenv('API_KEY')

@app.get('/hello')
def hello():
    return {'message': 'Hello from FastAPI!'}

@app.get('/api/weather')
def get_weather(city: str):
    url = (
        f'https://api.openweathermap.org/data/2.5/weather'
        f'?q={city}&appid={API_KEY}&units=metric'
    )

    response = requests.get(url)
    data = response.json()

    if data.get('cod') != 200:
        return {
            'status': 'error',
            'message': data.get('message', 'Unknown error')
        }

    filtered = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon'],
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed']
    }

    return filtered