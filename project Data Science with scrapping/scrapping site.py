import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

url = 'https://dom.ria.com/uk/prodazha-kvartir/chernovtsy/?page=17'

# Визначте ім'я файлу CSV
csv_file = 'house_ads.csv'

# Перевірка, чи файл існує
if os.path.isfile(csv_file):
    # Завантаження існуючого CSV файл у DataFrame
    df = pd.read_csv(csv_file)
else:
    # DataFrame
    df = pd.DataFrame(columns=['title', 'price', 'squer', 'room', 'city', 'addres', 'floor', 'metr', 'new_rem', 'auction', 'quiet_area', 'furniture', 'center', 'parking'])

# HTTP-запит для отримання вмісту сторінки
response = requests.get(url)

# чи запит вдалий
if response.status_code != 200:
    print("Не вдалося отримати сторінку. HTTP-помилка", response.status_code)
    exit()

#  об'єкт BeautifulSoup для розбору сторінки
soup = BeautifulSoup(response.text, 'html.parser')

# Знайдіть всі оголошення на сторінці
ads = soup.find_all('div', class_='wrap_desc p-rel')

# Перегляньте кожне оголошення та додайте дані до DataFrame
for ad in ads:
    title = ad.find('h2', class_='tit').text.strip()

    # Перевірка, чи такий title вже існує в DataFrame
    if title in df['title'].values:
        continue 
    
    price = ad.find('b', class_='size22').text.strip()
    
    element_div = ad.find_all('div', class_='label-border')
    new_a_elements = ad.find_all('a', class_='p-rel')
    a_elements = ad.find_all('a', class_='mb-5 i-block p-rel')
    span_elements = ad.find_all('span', class_='point-before')
 
    if "Новий ремонт" in [el.text.strip() for el in new_a_elements]:
        auction = 1
    else:
        auction = 0

    if "Торг можливий" in [el.text.strip() for el in element_div]:
        new_rem = 1
    else:
        new_rem = 0
    
    if "Спокійний район" in [el.text.strip() for el in element_div]:
        quiet_area = 1
    else:
        quiet_area = 0
    if "З меблями" in [el.text.strip() for el in new_a_elements]:
        furniture = 1
    else:
        furniture = 0

    if "У центрі" in [el.text.strip() for el in new_a_elements]:
        center = 1
    else:
        center = 0
    if "З парковкою" in [el.text.strip() for el in element_div]:
        parking = 1
    else:
        parking = 0
    if len(a_elements) > 1:
        desired_city = a_elements[1].text.strip()
        city = desired_city
    else:
        city = '-'

    desired_addres = a_elements[0]
   
    desired_floor = span_elements[3]
    desired_squer = span_elements[2]
    desired_room = span_elements[1]
    desired_m = span_elements[0]
    
    squer = desired_squer.text.strip()
    room = desired_room.text.strip()
    floor = desired_floor.text.strip()
    m = desired_m.text.strip()
    addres = desired_addres.text.strip()

    ad_data = {
        'title': title,
        'price': price,
        'squer': squer,
        'room': room,
        'city': city,
        'addres': addres,
        'floor': floor,
        'metr': m,
        'new_rem': new_rem,
        'auction': auction,
        'quiet_area': quiet_area,
        'furniture': furniture,
        'center': center,
        'parking': parking
    }

    # Створити новий DataFrame для кожного оголошення і додати його до існуючого
    
    new_row = pd.DataFrame([ad_data])
    df = pd.concat([df, new_row], ignore_index=False)
    



    

# ...

# Збережіть дані у CSV файл (режим додавання)
df.to_csv(csv_file, mode='w', index=False)
print("Нові дані було додано до", csv_file, url)

