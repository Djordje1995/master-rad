import pandas as pd
import constant
import numpy as np
import csv_handler

data = pd.read_csv(constant.DATA_FOLDER + constant.FULL_DATA_SERBIAN + constant.CSV)
data_features = ['Marka', 'Model', 'Godište', 'Kilometraža', 'Karoserija', 'Gorivo', 'Kubikaža',
                 'Snaga motora', 'Emisiona klasa motora', 'Pogon', 'Menjač', 'Cena']

MARKA = 'Marka'
MODEL = 'Model'
GODISTE = 'Godište'
KILOMETRAZA = 'Kilometraža'
KAROSERIJA = 'Karoserija'
GORIVO = 'Gorivo'
KUBIKAZA = 'Kubikaža'
SNAGA_MOTORA = 'Snaga motora'
EMISIONA_KLASA_MOTORA = 'Emisiona klasa motora'
POGON = 'Pogon'
MENJAC = 'Menjač'
CENA = 'Cena'

brand_median_list = {}
model_median_list = {}
year_median_list = {}
mileage_median_list = {}
car_body_median_list = {}
engine_power_median_list = {}
emission_class_median_list = {}
drive_median_list = {}
transmission_median_list = {}
fuel_type_median_list = {}
engine_size_median_list = {}

all_median_list = {}
all_percentage_median_list = {}
appended_module_median_list = {}


def calculate_median_per_column_value(column_data, column_median_list, column_name):
    column_data_array = column_data[CENA].to_numpy()
    sorted_data_array = np.sort(column_data_array)
    index = len(sorted_data_array) / 2
    frac = index - int(index)
    if frac == 0.0:
        median = (sorted_data_array[int(index - 1)] + sorted_data_array[int(index)]) / 2
    else:
        median = sorted_data_array[int(index - 0.5)]
    column_median_list[column_name] = median


def get_grouped_data_by_column(column):
    switcher = {
        # MARKA: data[MARKA],
        MODEL: data[MODEL],
        GODISTE: data[GODISTE],
        KILOMETRAZA: data[KILOMETRAZA],
        KAROSERIJA: data[KAROSERIJA],
        GORIVO: data[GORIVO],
        KUBIKAZA: data[KUBIKAZA],
        SNAGA_MOTORA: data[SNAGA_MOTORA],
        EMISIONA_KLASA_MOTORA: data[EMISIONA_KLASA_MOTORA],
        POGON: data[POGON],
        MENJAC: data[MENJAC],
        CENA: data[CENA]
    }
    return data.groupby(switcher.get(column))


def calculate_avg(column):
    column_data = list(data[column])
    count = 0
    summ = 0
    for item in column_data:
        summ += item
        count += 1
    return summ / count


def calculate_median_overall(column):
    column_data = list(data[column])
    column_data.sort()
    index = len(column_data) / 2
    frac = index - int(index)
    if frac == 0.0:
        return (column_data[int(index - 1)] + column_data[int(index)]) / 2
    else:
        return column_data[int(index - 0.5)]


def select_distinct_column(column_name):
    serbian_data = csv_handler.get_full_data_serbian()
    distinct_column_list = []
    for row in serbian_data:
        if row[column_name] not in distinct_column_list:
            distinct_column_list.append(row[column_name])
    return distinct_column_list


def calculate_median(column, median_list):
    grouped = get_grouped_data_by_column(column)
    column_list = select_distinct_column(column)
    for item in column_list:
        column_data = grouped.get_group(item)
        calculate_median_per_column_value(column_data, median_list, item)


def get_distinct_values(data_frame, column):
    return data_frame[column].unique().tolist()


def populate_median_lists():
    # calculate_median(MARKA, brand_median_list)
    calculate_median(MODEL, model_median_list)
    calculate_median(GODISTE, year_median_list)
    calculate_median(KILOMETRAZA, mileage_median_list)
    # calculate_median(KAROSERIJA, car_body_median_list)
    # calculate_median(GORIVO, fuel_type_median_list)
    calculate_median(KUBIKAZA, engine_size_median_list)
    calculate_median(SNAGA_MOTORA, engine_power_median_list)
    # calculate_median(EMISIONA_KLASA_MOTORA, emission_class_median_list)
    # calculate_median(POGON, drive_median_list)
    # calculate_median(MENJAC, transmission_median_list)


def fill_all_median_list():
    # all_median_list[MARKA] = brand_median_list
    all_median_list[MODEL] = model_median_list
    all_median_list[GODISTE] = year_median_list
    all_median_list[KILOMETRAZA] = mileage_median_list
    # all_median_list[KAROSERIJA] = car_body_median_list
    # all_median_list[GORIVO] = fuel_type_median_list
    all_median_list[KUBIKAZA] = engine_size_median_list
    all_median_list[SNAGA_MOTORA] = engine_power_median_list
    # all_median_list[EMISIONA_KLASA_MOTORA] = emission_class_median_list
    # all_median_list[POGON] = drive_median_list
    # all_median_list[MENJAC] = transmission_median_list


def calculate_median_percentages_per_list(median_list):
    total = 0
    n = 0
    percentage_list = {}
    for item in median_list:
        total += median_list[item]
        n += 1
    for item in median_list:
        percentage_list[item] = round((median_list[item] / total) * 100, 2)

    return percentage_list


def calculate_median_percentages():
    for median_list in all_median_list.keys():
        percentage_list = calculate_median_percentages_per_list(all_median_list[median_list])
        all_percentage_median_list[median_list] = percentage_list


def populate_lists():
    populate_median_lists()
    fill_all_median_list()
    calculate_median_percentages()


def get_median_lists():
    return all_median_list


def get_median_percentage_lists():
    return all_percentage_median_list


def get_median_list(median_list):
    return all_median_list[median_list]


def get_median_percentage_list(median_list):
    return all_percentage_median_list[median_list]
