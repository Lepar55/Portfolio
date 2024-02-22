
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service

def get_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver



def extract_emails_from_facebook_urls(urls):
    driver = get_driver()
    emails = []

    for url in urls:
        if pd.isnull(url) or url == 0:  # Перевіряємо, чи є значення нульовим або відсутнє
            emails.append({"email": 0})
            continue

        # Додаткова перевірка на наявність посилання на Facebook
        if 'facebook.com' not in url:
            emails.append({"email": 0})
            continue

        driver.get(url)
        time.sleep(5)

        resp = driver.page_source
        soup = BeautifulSoup(resp, 'html.parser')

        items = soup.find_all('div', {'class': 'x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1qughib x1qjc9v5 xozqiw3 x1q0g3np x1pi30zi x1swvt13 xyamay9 xykv574 xbmpl8g x4cne27 xifccgj'})

        if len(items) < 2: 
            emails.append({"email": 0})
            continue

        allDetails = items[1].find_all("span", {"class": "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h"}) 

        email_found = False  

        for contact in allDetails:
            if '@' in contact.text:
                emails.append({"email": contact.text})
                email_found = True
                break  

        if not email_found:
            emails.append({"email": 0})

    driver.quit()
    return emails


def main():
    data = pd.read_csv('urls.csv') 
    urls = data['facebook']

    emails = extract_emails_from_facebook_urls(urls)

    emails_df = pd.DataFrame(emails)
    data['emails'] = emails_df['email']

    data.to_csv('urls.csv', index=False)
    print("Електронні адреси було додано до файлу 'url.csv'")

if __name__ == "__main__":
    main()
