import customtkinter as ctk
from customtkinter import CTkImage
from customtkinter import FontManager
from PIL import Image
import requests
import os
from dotenv import load_dotenv
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ICONS
ICON_FILES = {
    'Clear': 'weathergui/icons/clear.png',
    'Clouds': 'weathergui/icons/clouds.png',
    'Rain': 'weathergui/icons/rain.png',
    'Drizzle': 'weathergui/icons/rain.png',
    'Thunderstorm': 'weathergui/icons/storm.png',
    'Snow': 'weathergui/icons/snow.png',
    'Mist': 'weathergui/icons/mist.png',
    'Fog': 'weathergui/icons/mist.png',
    'Haze': 'weathergui/icons/mist.png'
}

# API
load_dotenv()
API_KEY = os.getenv('YOUR_API_KEY')
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

# FUNCTIONS
def slide_up(widget, start_y, end_y, duration=300):
    frames = 12
    delta = (start_y - end_y) / frames
    delay = duration // frames

    def animate(frame=0):
        if frame >= frames:
            widget.place_configure(y=end_y)
            return
        new_y = start_y - delta * frame
        widget.place_configure(y=int(new_y))

        widget.after(delay, lambda: animate(frame + 1))

    animate()

def get_advice(temp, weather_main, wind):

    if temp < 0:
        return 'Bardzo zimno - załóż czapkę i rękawiczki.'
    if temp < 10:
        return 'Chłodno - przyda się kurtka.'
    if temp > 30:
        return 'Gorąco - pij dużo wody.'
    
    if weather_main in ['Rain', 'Drizzle']:
        return 'Pada deszcz - weź parasol.'
    if weather_main == 'Snow':
        return 'Śnieg - uważaj, może być slisko.'
    if weather_main == 'Thunderstorm':
        return 'Burza - zostań w domu, jeśli możesz.'
    if weather_main in ['Mist', 'Fog']:
        return 'Mgła - zachowaj ostrożność na drodze.'
    
    if wind > 10:
        return 'Mocny wiatr - uważaj na podmuchy.'
    return 'Pogoda w porządku - miłego dnia!'

def get_temp_color(temp):

    if temp < 0:
        return '#8ab4ff'
    if temp < 10:
        return '#b8c6ff'
    if temp < 20:
        return '#d7c8ff'
    if temp < 30:
        return '#c7a8ff'
    return '#ff8ad4'
    
def get_weather():

    city = entry.get()

    params = {
    'q': city,
    'appid': API_KEY,
    'units': 'metric',
    'lang': 'pl'
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code != 200:
            desc_label.configure(text='Nie znaleziono miasta.')
            return
        
        temp = data['main']['temp']
        desc = data['weather'][0]['description']

        weather_main = data['weather'][0]['main']
        wind = data['wind']['speed']

        if weather_main in ICON_FILES:
            icon_path = ICON_FILES[weather_main]
            icon_img = load_icon(icon_path)
            icon_label.configure(image=icon_img)
            icon_label.image = icon_img
        else:
            icon_label.configure(image=None)

        city_label.configure(text=city)

        color = get_temp_color(temp)
        temp_label.configure(
            text=f'{temp}°C', text_color=color)
        
        desc_label.configure(text=desc)

        advice = get_advice(temp, weather_main, wind)
        advice_label.configure(text=advice)

        slide_up(city_label, 320, 290)
        city_label.after(80, lambda: slide_up(temp_label, 375, 345))
        city_label.after(160, lambda: slide_up(desc_label, 425, 395))
        city_label.after(240, lambda: slide_up(icon_label, 490, 460))
        city_label.after(320, lambda: slide_up(advice_label, 570, 540))

    except Exception as e:
        city_label.configure(text='')
        temp_label.configure(text='')
        desc_label.configure(text=f'Błąd: {e}')
        icon_label.configure(image=None)
        icon_label.image = None
        advice_label.configure(text='')

def load_icon(path):
    img = Image.open(path)
    return CTkImage(light_image=img, dark_image=img, size=(100,100))

# GUI
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme(os.path.join(BASE_DIR, 'themes', 'google_dark.json'))

with open(os.path.join(BASE_DIR, 'themes', 'google_dark.json')) as f:
    theme = json.load(f)

root = ctk.CTk()
root.title('Pogoda')
root.geometry('420x680')
root.resizable(False, False)

FontManager.load_font(os.path.join(BASE_DIR, 'fonts', 'Inter-Regular.ttf'))
FontManager.load_font(os.path.join(BASE_DIR, 'fonts', 'Inter-Bold.ttf'))
FontManager.load_font(os.path.join(BASE_DIR, 'fonts', 'Inter-SemiBold.ttf'))

card_bg = ctk.CTkFrame(
    root, 
    width=380,
    height=640
)
card_bg.place(
    relx=0.5,
    rely=0.5,
    anchor='center'
)

title_label = ctk.CTkLabel(
    card_bg,
    text='Pogoda',
    font=ctk.CTkFont(**theme['CustomFonts']['title'])
)
title_label.place(
    relx=0.5,
    y=50,
    anchor='center'
)

subtitle_label = ctk.CTkLabel(
    card_bg,
    text='Wpisz miasto, aby sprawdzić pogodę',
    font=ctk.CTkFont(**theme['CustomFonts']['advice'])
)
subtitle_label.place(
    relx=0.5,
    y=95,
    anchor='center'
)
subtitle_label.configure(
    text_color=theme['TextColors']['tertiary']
)

entry = ctk.CTkEntry(
    card_bg,
    placeholder_text='Wpisz miasto',
    width=280,
    height=48
)
entry.place(
    relx=0.5,
    y=160,
    anchor='center'
)

button = ctk.CTkButton(
    card_bg,
    text='Pobierz pogodę',
    command=get_weather,
    width=220,
    height=48
)
button.place(
    relx=0.5,
    y=215,
    anchor='center'
)

city_label = ctk.CTkLabel(
    card_bg,
    text='',
    font=ctk.CTkFont(**theme['CustomFonts']['city'])
)
city_label.place(
    relx=0.5,
    y=290,
    anchor='center'
)

temp_label = ctk.CTkLabel(
    card_bg,
    text='',
    font=ctk.CTkFont(**theme['CustomFonts']['temp'])
)
temp_label.place(
    relx=0.5,
    y=345,
    anchor='center'
)

desc_label = ctk.CTkLabel(
    card_bg,
    text='',
    font=ctk.CTkFont(**theme['CustomFonts']['desc'])
)
desc_label.place(
    relx=0.5,
    y=395,
    anchor='center'
)
desc_label.configure(
    text_color=theme['TextColors']['secondary']
)

icon_label = ctk.CTkLabel(
    card_bg,
    text=''
)
icon_label.place(
    relx=0.5,
    y=460,
    anchor='center'
)

advice_label = ctk.CTkLabel(
    card_bg,
    text='',
    font=ctk.CTkFont(**theme['CustomFonts']['advice'])
)
advice_label.place(
    relx=0.5,
    y=540,
    anchor='center'
)
advice_label.configure(
    text_color=theme['TextColors']['tertiary']
)

root.mainloop()