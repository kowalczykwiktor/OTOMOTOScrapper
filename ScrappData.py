# coding: utf-8
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

url =
link_items_as_href = ['Oferta od', 'Kategoria', 'Marka pojazdu', 'Model pojazdu', 'Rodzaj paliwa', 'Napęd', 'Typ', 'Kolor',
                      'Metalik', 'Perłowy', 'VAT marża', 'Kraj pochodzenia', 'Pierwszy właściciel', 'Serwisowany w ASO', 'Stan',
                      'Wersja', 'Skrzynia biegów', 'Bezwypadkowy', 'Akryl (niemetalizowany)', 'Faktura VAT', 'Zarejestrowany w Polsce',
                      'Używane', 'Filtr cząstek stałych', 'Kod Silnika', 'Możliwość finansowania', 'Leasing', 'Uszkodzony', 'Tuning',
                      'Matowy', 'Homologacja ciężarowa', 'Zarejestrowany jako zabytek', 'Kierownica po prawej (Anglik)']
convert_to_int = ['Liczba drzwi', 'Liczba miejsc', 'Rok produkcji']
