# ./SynologyDrive/Repository/OTOMOTOScrapper

# pip install -U pip

# pip install -U requests
# pip install -U time
# pip install -U bs4
# pip install -U pymongo

import requests
import time
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://wiktorkowalczyk:pjatk2019@cluster0-bqxx3.mongodb.net/')
db = client.otomoto
offers = db.offers
print(client.list_database_names())

url = ''
link_items_as_href = ['Oferta od', 'Kategoria', 'Marka pojazdu', 'Model pojazdu', 'Rodzaj paliwa', 'Napęd', 'Typ', 'Kolor',
                      'Metalik', 'Perłowy', 'VAT marża', 'Kraj pochodzenia', 'Pierwszy właściciel', 'Serwisowany w ASO', 'Stan',
                      'Wersja', 'Skrzynia biegów', 'Bezwypadkowy', 'Akryl (niemetalizowany)', 'Faktura VAT', 'Zarejestrowany w Polsce',
                      'Używane', 'Filtr cząstek stałych', 'Kod Silnika', 'Możliwość finansowania', 'Leasing', 'Uszkodzony', 'Tuning',
                      'Matowy', 'Homologacja ciężarowa', 'Zarejestrowany jako zabytek', 'Kierownica po prawej (Anglik)']
convert_to_int = ['Liczba drzwi', 'Liczba miejsc', 'Rok produkcji']

pages = 6400
count = 0

for page in range(1, pages):
    response = requests.get(url + str(page))
    soup = BeautifulSoup(response.text, 'html.parser')
    contents = soup.findAll('div', class_='offer-item__content')

    for content in contents:
        db_record = {}
        link = content.find('a', class_='offer-title__link')
        link_url = link.get('href')
        link_response = requests.get(link_url)
        print(link_url)
        link_soup = BeautifulSoup(link_response.text, 'html.parser')
        link_date_and_id = link_soup.find(
            'div', class_='offer-content__rwd-metabar').findAll('span', class_='offer-meta__value')
        link_id = link_date_and_id[1].text.strip()
        print(link_id)
        if (offers.find_one({'otomoto_id': link_id})):
            print('NOT SAVED')
            continue