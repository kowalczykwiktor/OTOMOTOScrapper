# ./SynologyDrive/Repository/OTOMOTOScrapper

# pip3 install -U pip

# pip3 install -U requests
# pip3 install -U time
# pip3 install -U bs4
# pip3 install -U pymongo
# pip3 install -U dnspython

import requests
import time
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient
client = MongoClient(
    'mongodb+srv://wiktorkowalczyk:pjatk2019@cluster0-bqxx3.mongodb.net/')
db = client.otomoto
offers = db.offers
print('/////////////////////////////////////////////////..::Connection Successfully::../////////////////////////////////////////////////////')
print('Available databases:')
print(client.list_database_names())
print('/////////////////////////////////////////////////..::Scraping started::../////////////////////////////////////////////////////')
url = 'https://www.otomoto.pl/osobowe/?search%5Border%5D=created_at_first%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=&page='
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
        try:
            link_date_and_id = link_soup.find(
                'div', class_='offer-content__rwd-metabar').findAll('span', class_='offer-meta__value')
        except AttributeError as ServiceError:
            continue
        link_id = link_date_and_id[1].text.strip()
        print(link_id)
        if (offers.find_one({'otomoto_id': link_id})):
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..::Offer not saved::..<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            continue
        link_date = link_date_and_id[0].text.strip()
        print(link_date)
        try:
            location = content.find(
                'span', class_='offer-item__location').h4.text.split('(')
        except AttributeError as ServiceError:
            continue
        city = location[0].strip()
        state = location[1].replace(')', '').strip()
        print(city)
        print(state)
        price = content.find('span', class_='offer-price__number').text.replace(
            'PLN', '').replace(' ', '').replace('\n', '')
        print(price)
        if ('EUR' in price):
            price = int(float(price.replace('EUR', '').replace(',', '.'))*4.26)
        elif ('USD' in price):
            price = int(float(price.replace('USD', '').replace(',', '.'))*3.82)
        else:
            price = int(float(price.replace(',', '.')))
        link_items = link_soup.findAll('li', class_='offer-params__item')
        for link_item in link_items:
            key = link_item.span.text.strip()
            value = link_item.div
            print(key)
            if (key in link_items_as_href):
                print(value.a.text.strip())
                if (value.a.text.strip() == 'Tak'):
                    db_record.update({key: 1})
                else:
                    db_record.update({key: value.a.text.strip()})
            else:
                print(value.text.strip())
                if (key == 'Przebieg'):
                    db_record.update(
                        {key: int(value.text.replace('km', '').replace(' ', '').replace('\n', ''))})
                elif (key == 'Pojemność skokowa'):
                    db_record.update(
                        {key: int(value.text.replace('cm3', '').replace(' ', '').replace('\n', ''))})
                elif (key == 'Moc'):
                    db_record.update(
                        {key: int(value.text.replace('KM', '').replace(' ', '').replace('\n', ''))})
                elif (key == 'Emisja CO2'):
                    db_record.update(
                        {key: int(value.text.replace('g/km', '').replace(' ', '').replace('\n', ''))})
                elif (key in convert_to_int):
                    db_record.update({key: int(value.text.strip())})
                else:
                    db_record.update({key: value.text.strip()})
        features = link_soup.find('div', class_='offer-features')
        if (features != None):
            features = features.findAll('li', class_='offer-features__item')
            for feature in features:
                feature = 'Posiada: ' + feature.text.strip()
                print(feature)
                db_record.update({feature: 1})
        description = link_soup.find(
            'div', class_='offer-description').div.text.strip()
        print(description)
        print(link_url)
        db_record.update({'Otomoto id': link_id,
                          'Data publikacji': link_date,
                          'Cena': price,
                          'Miasto': city,
                          'Wojewodztwo': state,
                          'Url': link_url,
                          'Opis': description})
        offers.insert_one(db_record)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..::Offer Saved::..<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        count += 1
        print(count)
        time.sleep(0.5)
print('////////////////////////////////////////////////..::Scraping ended::..///////////////////////////////////////////////////////')