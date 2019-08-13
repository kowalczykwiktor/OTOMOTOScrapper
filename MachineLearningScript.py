# ./SynologyDrive/Repository/OTOMOTOScrapper

# pip3 install -U pandas
# pip3 install -U matplotlib
# pip3 install -U sklearn
# pip3 install -U simplefilter

from pymongo import MongoClient
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import BaggingRegressor
from datetime import datetime
from warnings import simplefilter

simplefilter(action='ignore', category=FutureWarning)
startTime = datetime.now()
client = MongoClient(
    'mongodb+srv://wiktorkowalczyk:pjatk2019@cluster0-bqxx3.mongodb.net/')
db = client.otomoto
offers = db.offers
print('/////////////////////////////////////////////////..::Connection Successfully::../////////////////////////////////////////////////////')
print('Available databases:')
print(client.list_database_names())
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..::Machine Learning started::..<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
df = pd.DataFrame(list(offers.find())).fillna(0)
columns_list = df.columns.tolist()
categorical_columns = ['Marka pojazdu', 'Model pojazdu', 'Kategoria', 'Kolor', 'Kraj pochodzenia', 'Napęd', 'Oferta od', 'Rodzaj paliwa', 'Skrzynia biegów', 'Stan', 'Typ', 'Wersja', 'Miasto', 'Wojewodztwo']
list_of_columns = ['Akryl (niemetalizowany)', 'Bezwypadkowy', 'Emisja CO2', 'Faktura VAT', 'Filtr cząstek stałych', 'Leasing', 'Homologacja ciężarowa', 'Kierownica po prawej (Anglik)', 'Liczba drzwi', 'Liczba miejsc', 'Metalik', 'Matowy', 'Moc', 'Możliwość finansowania', 'Perłowy', 'Pierwszy właściciel', 'Pojemność skokowa', 'Przebieg', 'Rok produkcji', 'Serwisowany w ASO', 'Tuning', 'Uszkodzony', 'VAT marża', 'Posiada: ABS', 'Posiada: ASR (kontrola trakcji)', 'Posiada: Alarm', 'Posiada: Alufelgi', 'Posiada: Isofix', 'Posiada: Asystent parkowania', 'Posiada: Asystent pasa ruchu', 'Posiada: Bluetooth', 'Posiada: MP3', 'Posiada: CD', 'Posiada: Centralny zamek', 'Posiada: Czujnik deszczu', 'Posiada: Hak', 'Posiada: Czujnik martwego pola', 'Posiada: Czujnik zmierzchu', 'Posiada: Czujniki parkowania przednie', 'Posiada: Czujniki parkowania tylne', 'Posiada: Dach panoramiczny', 'Posiada: ESP (stabilizacja toru jazdy)', 'Posiada: Elektrochromatyczne lusterka boczne', 'Posiada: Elektrochromatyczne lusterko wsteczne', 'Posiada: Elektryczne szyby przednie', 'Posiada: Elektryczne szyby tylne', 'Posiada: Gniazdo USB', 'Posiada: Elektrycznie ustawiane fotele', 'Posiada: Elektrycznie ustawiane lusterka', 'Posiada: Gniazdo AUX', 'Posiada: Gniazdo SD', 'Posiada: HUD (wyświetlacz przezierny)', 'Posiada: Immobilizer', 'Posiada: Kamera cofania', 'Posiada: Klimatyzacja automatyczna', 'Posiada: Klimatyzacja czterostrefowa', 'Posiada: Klimatyzacja dwustrefowa', 'Posiada: Klimatyzacja manualna', 'Posiada: Komputer pokładowy', 'Posiada: Kurtyny powietrzne', 'Posiada: Nawigacja GPS', 'Posiada: Odtwarzacz DVD', 'Zarejestrowany w Polsce', 'Posiada: Ogranicznik prędkości', 'Posiada: Ogrzewanie postojowe', 'Posiada: Podgrzewana przednia szyba', 'Posiada: Podgrzewane lusterka boczne', 'Posiada: Podgrzewane przednie siedzenia', 'Posiada: Radio fabryczne', 'Posiada: Podgrzewane tylne siedzenia', 'Posiada: Poduszka powietrzna chroniąca kolana', 'Posiada: Tuner TV', 'Posiada: Poduszka powietrzna kierowcy', 'Posiada: Poduszka powietrzna pasażera', 'Posiada: Przyciemniane szyby', 'Posiada: Poduszki boczne przednie', 'Posiada: Poduszki boczne tylne', 'Posiada: Radio niefabryczne', 'Posiada: Regulowane zawieszenie', 'Posiada: Relingi dachowe', 'Posiada: System Start-Stop', 'Posiada: Szyberdach', 'Posiada: Tapicerka skórzana', 'Posiada: Tapicerka welurowa', 'Posiada: Tempomat', 'Posiada: Tempomat aktywny', 'Posiada: Wielofunkcyjna kierownica', 'Posiada: Wspomaganie kierownicy', 'Posiada: Zmieniarka CD', 'Posiada: Łopatki zmiany biegów', 'Posiada: Światła LED', 'Posiada: Światła Xenonowe', 'Posiada: Światła do jazdy dziennej', 'Posiada: Światła przeciwmgielne', 'Zarejestrowany jako zabytek']
label = df['Cena']
for item in df['Akryl (niemetalizowany)']:
    if isinstance(item, str):
        df = df.replace(item, '1')
for item in df['Matowy']:
    if isinstance(item, str):
        df = df.replace(item, '1')
for item in df['Metalik']:
    if isinstance(item, str):
        df = df.replace(item, '1')
df['Akryl (niemetalizowany)'] = df['Akryl (niemetalizowany)'].astype('int')
df['Matowy'] = df['Matowy'].astype('int')
df['Metalik'] = df['Metalik'].astype('int')
for column in categorical_columns:
    unique_values = list(set(df[column]))
    mapping = {}
    for value in unique_values:
        mapping.update({value: unique_values.index(value)})
    df[column] = df[column].replace(mapping)
final_columns_list = list_of_columns + categorical_columns
train_data = df[final_columns_list]
x_train, x_test, y_train, y_test = train_test_split(
    train_data, label, test_size=0.1, random_state=2)

# LinearRegression:
linear_regression = LinearRegression()
linear_regression.fit(x_train, y_train)
lr_score = linear_regression.score(x_test, y_test)
print('LinearRegression score: ' + str(lr_score))

# MLPRegressor:
mlp_regressor = MLPRegressor()
mlp_regressor.fit(x_train, y_train)
mlpr_score = mlp_regressor.score(x_test, y_test)
print('MLPRegressor score: ' + str(mlpr_score))

# GradientBoostingRegressor:
gradient_boosting_regressor = GradientBoostingRegressor()
gradient_boosting_regressor.fit(x_train, y_train)
gb_score = gradient_boosting_regressor.score(x_test, y_test)
print('GradientBoostingRegressor score: ' + str(gb_score))

# DecisionTreeRegressor:
decision_tree_regressor = DecisionTreeRegressor()
decision_tree_regressor.fit(x_train, y_train)
dt_score = decision_tree_regressor.score(x_test, y_test)
print('DecisionTreeRegressor score: ' + str(dt_score))

# ExtraTreesRegressor:
extra_trees_regressor = ExtraTreesRegressor()
extra_trees_regressor.fit(x_train, y_train)
et_score = extra_trees_regressor.score(x_test, y_test)
print('ExtraTreesRegressor score: ' + str(et_score))

# BaggingRegressor:
bagging_regressor = BaggingRegressor()
bagging_regressor.fit(x_train, y_train)
b_score = bagging_regressor.score(x_test, y_test)
print('BaggingRegressor score: ' + str(b_score))

# RandomForestRegressor:
random_forest_regressor = RandomForestRegressor()
random_forest_regressor.fit(x_train, y_train)
rf_score = random_forest_regressor.score(x_test, y_test)
print('RandomForestRegressor score: ' + str(rf_score))

# RandomForestRegressor No2:
random_forest_regressor = RandomForestRegressor(
    max_depth=5, random_state=0, n_estimators=100)
random_forest_regressor.fit(x_train, y_train)
rf_score_1 = random_forest_regressor.score(x_test, y_test)
print('RandomForestRegressor No2 score: ' + str(rf_score_1))

# RandomForestRegressor No3:
random_forest_regressor = RandomForestRegressor(
    max_depth=200, random_state=100, n_estimators=50)
random_forest_regressor.fit(x_train, y_train)
rf_score_2 = random_forest_regressor.score(x_test, y_test)
print('RandomForestRegressor No3 score: ' + str(rf_score_2))
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..::Machine Learning ended::..<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
print('Process time:')
print(datetime.now() - startTime)