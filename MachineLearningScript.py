# ./SynologyDrive/Repository/OTOMOTOScrapper

# pip install -U pandas
# pip install -U matplotlib
# pip install -U sklearn

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
client = MongoClient(
    'mongodb+srv://wiktorkowalczyk:pjatk2019@cluster0-bqxx3.mongodb.net/')
db = client.otomoto
offers = db.offers
print('/////////////////////////////////////////////////..::Connection Successfully::../////////////////////////////////////////////////////')
print(client.list_database_names())
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..::MachineLearning started::..<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
df = pd.DataFrame(list(offers.find())).fillna(0)
columns_list = df.columns.tolist()
categorical_columns = ['Marka pojazdu', 'Model pojazdu', 'Kategoria', 'Kolor', 'Kraj pochodzenia', 'Napęd',
                       'Oferta od', 'Rodzaj paliwa', 'Skrzynia biegów', 'Stan', 'Typ', 'Wersja', 'Miasto', 'Wojewodztwo']
list_of_columns = ['Akryl (niemetalizowany)', 'Bezwypadkowy', 'Emisja CO2', 'Faktura VAT', 'Filtr cząstek stałych', 'Leasing', 'Homologacja ciężarowa', 'Kierownica po prawej (Anglik)', 'Liczba drzwi', 'Liczba miejsc', 'Metalik', 'Matowy', 'Moc', 'Możliwość finansowania', 'Perłowy', 'Pierwszy właściciel', 'Pojemność skokowa', 'Przebieg', 'Rok produkcji', 'Serwisowany w ASO', 'Tuning', 'Uszkodzony', 'VAT marża', 'Wyposażenie: ABS', 'Wyposażenie: ASR (kontrola trakcji)', 'Wyposażenie: Alarm', 'Wyposażenie: Alufelgi', 'Wyposażenie: Isofix', 'Wyposażenie: Asystent parkowania', 'Wyposażenie: Asystent pasa ruchu', 'Wyposażenie: Bluetooth', 'Wyposażenie: MP3', 'Wyposażenie: CD', 'Wyposażenie: Centralny zamek', 'Wyposażenie: Czujnik deszczu', 'Wyposażenie: Hak', 'Wyposażenie: Czujnik martwego pola', 'Wyposażenie: Czujnik zmierzchu', 'Wyposażenie: Czujniki parkowania przednie', 'Wyposażenie: Czujniki parkowania tylne', 'Wyposażenie: Dach panoramiczny', 'Wyposażenie: ESP (stabilizacja toru jazdy)', 'Wyposażenie: Elektrochromatyczne lusterka boczne', 'Wyposażenie: Elektrochromatyczne lusterko wsteczne', 'Wyposażenie: Elektryczne szyby przednie', 'Wyposażenie: Elektryczne szyby tylne', 'Wyposażenie: Gniazdo USB', 'Wyposażenie: Elektrycznie ustawiane fotele', 'Wyposażenie: Elektrycznie ustawiane lusterka', 'Wyposażenie: Gniazdo AUX', 'Wyposażenie: Gniazdo SD', 'Wyposażenie: HUD (wyświetlacz przezierny)', 'Wyposażenie: Immobilizer', 'Wyposażenie: Kamera cofania', 'Wyposażenie: Klimatyzacja automatyczna',
                   'Wyposażenie: Klimatyzacja czterostrefowa', 'Wyposażenie: Klimatyzacja dwustrefowa', 'Wyposażenie: Klimatyzacja manualna', 'Wyposażenie: Komputer pokładowy', 'Wyposażenie: Kurtyny powietrzne', 'Wyposażenie: Nawigacja GPS', 'Wyposażenie: Odtwarzacz DVD', 'Zarejestrowany w Polsce', 'Wyposażenie: Ogranicznik prędkości', 'Wyposażenie: Ogrzewanie postojowe', 'Wyposażenie: Podgrzewana przednia szyba', 'Wyposażenie: Podgrzewane lusterka boczne', 'Wyposażenie: Podgrzewane przednie siedzenia', 'Wyposażenie: Radio fabryczne', 'Wyposażenie: Podgrzewane tylne siedzenia', 'Wyposażenie: Poduszka powietrzna chroniąca kolana', 'Wyposażenie: Tuner TV', 'Wyposażenie: Poduszka powietrzna kierowcy', 'Wyposażenie: Poduszka powietrzna pasażera', 'Wyposażenie: Przyciemniane szyby', 'Wyposażenie: Poduszki boczne przednie', 'Wyposażenie: Poduszki boczne tylne', 'Wyposażenie: Radio niefabryczne', 'Wyposażenie: Regulowane zawieszenie', 'Wyposażenie: Relingi dachowe', 'Wyposażenie: System Start-Stop', 'Wyposażenie: Szyberdach', 'Wyposażenie: Tapicerka skórzana', 'Wyposażenie: Tapicerka welurowa', 'Wyposażenie: Tempomat', 'Wyposażenie: Tempomat aktywny', 'Wyposażenie: Wielofunkcyjna kierownica', 'Wyposażenie: Wspomaganie kierownicy', 'Wyposażenie: Zmieniarka CD', 'Wyposażenie: Łopatki zmiany biegów', 'Wyposażenie: Światła LED', 'Wyposażenie: Światła Xenonowe', 'Wyposażenie: Światła do jazdy dziennej', 'Wyposażenie: Światła przeciwmgielne', 'Zarejestrowany jako zabytek']
columns_list_not_to_be_used = ['_id', 'Data publikacji', 'Liczba pozostałych rat', 'Miesięczna rata', 'Numer rejestracyjny pojazdu',
                               'VIN', 'Kod Silnika', 'Opis', 'Opłata początkowa', 'Otomoto id', 'Pierwsza rejestracja', 'Url', 'Wartość wykupu']
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
    # column = column.decode('utf-8')
    unique_values = list(set(df[column]))
    mapping = {}
    for value in unique_values:
        mapping.update({value: unique_values.index(value)})
    df[column] = df[column].replace(mapping)
final_columns_list = map(lambda column: column, list_of_columns + categorical_columns)
# train_data = df[column].reindex(columns=final_columns_list)
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
print('////////////////////////////////////////////////..::MachineLearning ended::..///////////////////////////////////////////////////////')