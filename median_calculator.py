import pandas as pd
import constant
import percentage_value_maps
import numpy as np

data = pd.read_csv(constant.DATA_FOLDER + constant.LEARNING_DATA + constant.CSV)
data_features = [constant.BRAND, constant.MODEL, constant.YEAR, constant.TRANSMISSION, constant.MILEAGE,
                 constant.FUEL_TYPE, constant.TAX, constant.MPG, constant.ENGINE_SIZE]

brand_median_list = []
transmission_median_list = []
fuel_type_median_list = []
engine_size_median_list = []

audi_median_list = []
bmw_median_list = []
ford_median_list = []
hyundai_median_list = []
mercedes_median_list = []
skoda_median_list = []
toyota_median_list = []
vauxhall_median_list = []
vw_median_list = []


def get_model_median_list(brand):
    switcher = {
        constant.AUDI: audi_median_list,
        constant.BMW: bmw_median_list,
        constant.FORD: ford_median_list,
        constant.HYUNDI: hyundai_median_list,
        constant.MERCEDES: mercedes_median_list,
        constant.SKODA: skoda_median_list,
        constant.TOYOTA: toyota_median_list,
        constant.VAUXHALL: vauxhall_median_list,
        constant.VW: vw_median_list
    }
    return switcher.get(brand)


def calculate_median_per_column_value(column_data, column_median_list, column_name):
    column_data_array = column_data.price.to_numpy()
    sorted_data_array = np.sort(column_data_array)
    index = len(sorted_data_array) / 2
    if type(index) == int:
        median = {column_name: (sorted_data_array[index - 1] + sorted_data_array[index]) / 2}
    else:
        median = {column_name: sorted_data_array[int(index - 0.5)]}
    column_median_list.append(median)


def get_grouped_data_by_column(column):
    switcher = {
        constant.BRAND: data.brand,
        constant.MODEL: data.model,
        constant.YEAR: data.year,
        constant.TRANSMISSION: data.transmission,
        constant.MILEAGE: data.mileage,
        constant.FUEL_TYPE: data.fuelType,
        constant.TAX: data.tax,
        constant.MPG: data.mpg,
        constant.ENGINE_SIZE: data.engineSize
    }
    return data.groupby(switcher.get(column))


def calculate_median(column, median_list):
    grouped = get_grouped_data_by_column(column)
    column_list = percentage_value_maps.select_distinct_column(constant.LEARNING_DATA, column)
    for item in column_list:
        column_data = grouped.get_group(item)
        calculate_median_per_column_value(column_data, median_list, item)


def get_distinct_values(data_frame, column):
    return data_frame[column].unique().tolist()


def calculate_models_medians():
    brand_list = percentage_value_maps.select_distinct_column(constant.LEARNING_DATA, constant.BRAND)
    grouped_by_brand = get_grouped_data_by_column(constant.BRAND)
    for brand in brand_list:
        brand_data = grouped_by_brand.get_group(brand)
        model_list = get_distinct_values(brand_data, constant.MODEL)
        grouped_by_model = brand_data.groupby(constant.MODEL)
        for model in model_list:
            model_data = grouped_by_model.get_group(model)
            calculate_median_per_column_value(model_data, get_model_median_list(brand), model)


def populate_median_lists():
    calculate_median(constant.BRAND, brand_median_list)
    calculate_models_medians()
    calculate_median(constant.TRANSMISSION, transmission_median_list)
    calculate_median(constant.FUEL_TYPE, fuel_type_median_list)
    calculate_median(constant.ENGINE_SIZE, engine_size_median_list)


def print_median_lists():
    print(brand_median_list)
    print(transmission_median_list)
    print(fuel_type_median_list)
    print(engine_size_median_list)
    print("Models:")
    print(audi_median_list)
    print(bmw_median_list)
    print(ford_median_list)
    print(hyundai_median_list)
    print(mercedes_median_list)
    print(skoda_median_list)
    print(toyota_median_list)
    print(vauxhall_median_list)
    print(vw_median_list)


populate_median_lists()
print_median_lists()


def calculate_median_percentages_per_list():
    print("za svaki median list da se prebace u procentualnu vrednost zbog uporedjivanaj i sredjivanja modela")
