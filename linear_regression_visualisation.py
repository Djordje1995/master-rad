import matplotlib.scale
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import constant
import csv_handler
import percentage_value_maps

data = pd.read_csv(constant.DATA_FOLDER + constant.LEARNING_DATA + constant.CSV)
# data = csv_handler.read_csv(constant.LEARNING_DATA)

data_features = [constant.BRAND, constant.BR_MODEL, constant.YEAR, constant.TRANSMISSION, constant.MILEAGE,
                 constant.FUEL_TYPE, constant.TAX, constant.MPG, constant.ENGINE_SIZE]

data_frame = pd.DataFrame(data)

X = data[data_features]
Y = data[constant.PRICE]


def fetch_specific_brand_rows(brand):
    grouped = data.groupby(data.brand)
    return grouped.get_group(brand)


def show_model_relations():
    brand_list = percentage_value_maps.select_distinct_column(constant.BRAND)
    for brand in brand_list:
        brand_data = fetch_specific_brand_rows(brand)
        x = brand_data[data_features]
        y = brand_data[constant.PRICE]
        plt.figure(figsize=(25, 7))
        plt.scatter(x[constant.MODEL], y, alpha=0.3)
        plt.grid()
        plt.xlabel(brand)
        plt.ylabel(constant.PRICE)
        plt.show()


def get_ticks_2():
    return [0, 42, 84, 126, 168, 210, 252, 294, 336, 378, 420]


def sort_values_accordingly(column):
    return data.sort_values(by=[column], ascending=True)


def show_price_relation(column):
    plt.figure(figsize=(12, 7))

    sorted_data = sort_values_accordingly(column)
    x = sorted_data[data_features]
    y = sorted_data[constant.PRICE]
    plt.scatter(x[column], y, alpha=0.3)
    plt.grid()
    plt.xlabel(column)
    plt.ylabel(constant.PRICE)
    plt.show()


def fix(list_mpg):
    new_list = []
    for item in list_mpg:
        if item.find(","):
            new_item = item.replace(",", ".")
            new_list.append(new_item)
    new_arr = np.array(new_list).astype('float64')
    return np.sort(new_arr).tolist()


def every_tenth(mph_list):
    new_list = []
    initial = 0
    while initial <= len(mph_list):
        new_list.append(mph_list[initial])
        initial += 31
    return new_list


def get_ticks():
    sorted_data = data.sort_values(by=[constant.MPG])
    list_mpg = sorted_data[constant.MPG].unique().tolist()
    new_list = fix(list_mpg)
    return every_tenth(new_list)


def visualise_predicted_results(y_test, y_pred):
    plt.figure(figsize=(15, 10))
    plt.scatter(y_test, y_pred)
    plt.xlabel("Actual prices")
    plt.ylabel("Predicted prices")
    plt.title("Actual vs Predicted prices")
    plt.show()


# show_price_relation(constant.BRAND)
# show_model_relations()
# show_price_relation(constant.YEAR)
# show_price_relation(constant.TRANSMISSION)
# show_price_relation(constant.MILEAGE)
# show_price_relation(constant.FUEL_TYPE)
# show_price_relation(constant.TAX)
# show_price_relation(constant.MPG)
# show_price_relation(constant.ENGINE_SIZE)

