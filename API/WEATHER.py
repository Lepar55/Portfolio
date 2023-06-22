import requests
import json

api_key = 'dcb9c62e06593fa09368989ac264801f'
url = f'http://api.openweathermap.org/data/2.5/weather?q=Lviv&appid={api_key}'

try:
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']
        print(f'Температура: {temperature}K')
        print(f'Вологість: {humidity}%')
        print(f'Опис погоди: {description}')
    else:
        print('Не вдалося отримати погодні дані.')
        print(response.status_code)
except requests.exceptions.RequestException as e:
    print('Сталася помилка під час виконання запиту:', e)
