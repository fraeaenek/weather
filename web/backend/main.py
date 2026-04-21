from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv
import requests
from pathlib import Path

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
INDEX_FILE = os.path.join(STATIC_DIR, "index.html")

app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')

@app.get('/')
def root():
    return FileResponse(INDEX_FILE)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

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
        'temperature': round(data['main']['temp']),
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon'],
        'humidity': data['main']['humidity'],
        'wind': data['wind']['speed']
    }

    return filtered