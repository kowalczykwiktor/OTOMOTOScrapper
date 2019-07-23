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
