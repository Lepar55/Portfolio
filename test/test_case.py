



import pandas as pd
import re
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import os

MAX_RETRIES = 2
RETRY_DELAY = 1

def get_html_selenium(url):
    for _ in range(MAX_RETRIES):
        try:
            time.sleep(RETRY_DELAY)
            service = Service(ChromeDriverManager().install())  # Для безголовного режиму (необов'язково)
            driver = webdriver.Chrome(service=service)  # Запускаємо Chrome з встановленим драйвером та опціями
            driver.get(url)
            html = driver.page_source
            driver.quit()
            return html
        except Exception as e:
            print(f"Error fetching {url} with Selenium: {e}")
            print("Retrying...")
            continue
    print(f"Max retries exceeded for {url}. Skipping...")
    return None

# Функція для парсингу електронної пошти та посилань на соціальні мережі з HTML-коду, отриманого за допомогою Selenium
def parse_content_selenium(html):
    all_data = {
        'emails': [],
        'facebook': [],
        'youtube': [],
        'twitter': [],
        'instagram': []
    }
    
    if not html:
        return all_data  

    soup = BeautifulSoup(html, 'html.parser')

    # Ініціалізуємо змінні для перших знайдених посилань та пошти
    first_facebook_link = None
    first_youtube_link = None
    first_twitter_link = None
    first_instagram_link = None
    email = None

    # Проходимо через всі посилання на сторінці і додаємо перше знайдене посилання для кожної мережі
    for tag in soup.find_all(['a', 'p', 'span'], href=True):
        href = tag.get('href', '')
        text = tag.get_text()
       

        if 'facebook.com' in href and href.startswith('https://www.facebook.com'):
            if not first_facebook_link:
                first_facebook_link = href
        elif 'youtube.com' in href or 'youtu.be' in href:
            if not first_youtube_link:
                first_youtube_link = href
        elif 'twitter.com' in href:
            if not first_twitter_link:
                first_twitter_link = href
        elif 'instagram.com' in href:
            if not first_instagram_link:
                first_instagram_link = href

        # Пошук електронної пошти в тексті тегів <p> та <span>
        if not email:
            email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
            emails = re.findall(email_pattern, text)
            if emails:
                email = emails[0]

    # Перевіряємо, чи були знайдені посилання для кожної мережі
    first_facebook_link = first_facebook_link if first_facebook_link else '0'
    first_youtube_link = first_youtube_link if first_youtube_link else '0'
    first_twitter_link = first_twitter_link if first_twitter_link else '0'
    first_instagram_link = first_instagram_link if first_instagram_link else '0'

    all_data['emails'].append(email)
    all_data['facebook'].append(first_facebook_link)
    all_data['youtube'].append(first_youtube_link)
    all_data['twitter'].append(first_twitter_link)
    all_data['instagram'].append(first_instagram_link)

    return all_data



def write_to_csv(data, csv_file_write):
    try:
        if os.path.isfile(csv_file_write):
            df = pd.read_csv(csv_file_write)
        else:
            df = pd.DataFrame(columns=['emails', 'facebook', 'instagram', 'twitter', 'youtube'])

        new_df = pd.DataFrame(data)

        
        existing_emails = df['emails'].tolist()
        new_emails = new_df['emails'].tolist()
        unique_new_emails = [email for email in new_emails if email not in existing_emails]

        if unique_new_emails:
            df = pd.concat([df, new_df[new_df['emails'].isin(unique_new_emails)]], ignore_index=True)
            df.to_csv(csv_file_write, index=False)
            print(f"Data successfully written to {csv_file_write}")
        else:
            print("No new unique data found. Skipping writing to CSV.")

    except Exception as e:
        print(f"Error writing to CSV: {e}")


def read_urls_from_csv(file_path, column_name):
    try:
        df = pd.read_csv(file_path)
        urls = df[column_name].tolist()
        # Додати "https://" до URL-адрес, якщо вони не мають префікс
        urls = ['https://' + str(url) if isinstance(url, str) and not url.startswith('http') else str(url) for url in urls]
        return urls
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []

# Приклад використання
if __name__ == '__main__':
    csv_file_path = 'urls.csv'  
    column_name = 'website'  
    csv_file_write = 'addresses.csv'  

    urls = read_urls_from_csv(csv_file_path, column_name)

    for url in urls:
        if url and isinstance(url, str) and url.lower() != 'nan':
            html = get_html_selenium(url)
            if html is not None:
                print(url)
                data = parse_content_selenium(html)
                print(f"Data: {data}")
                
                write_to_csv(data, csv_file_write)
            else:
                print(f"HTML content is None for {url}. Skipping...")
                print(url)
                









