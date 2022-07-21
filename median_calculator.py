import pandas as pd
import constant
import percentage_value_maps
import numpy as np

data = pd.read_csv(constant.DATA_FOLDER + constant.LEARNING_DATA + constant.CSV)
data_features = [constant.BRAND, constant.BR_MODEL, constant.YEAR, constant.TRANSMISSION, constant.MILEAGE,
                 constant.FUEL_TYPE, constant.TAX, constant.MPG, constant.ENGINE_SIZE]
modules = [constant.AUDI, constant.BMW, constant.FORD, constant.HYUNDI, constant.MERCEDES, constant.SKODA,
           constant.TOYOTA, constant.VAUXHALL, constant.VW]


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

all_median_list = []
all_percentage_median_list = {}
appended_module_median_list = {}


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
    frac = index - int(index)
    if frac == 0.0:
        median = {column_name: (sorted_data_array[int(index - 1)] + sorted_data_array[int(index)]) / 2}
    else:
        median = {column_name: sorted_data_array[int(index - 0.5)]}
    column_median_list.append(median)


def get_grouped_data_by_column(column):
    switcher = {
        constant.BRAND: data.brand,
        constant.BR_MODEL: data.model,
        constant.YEAR: data.year,
        constant.TRANSMISSION: data.transmission,
        constant.MILEAGE: data.mileage,
        constant.FUEL_TYPE: data.fuelType,
        constant.TAX: data.tax,
        constant.MPG: data.mpg,
        constant.ENGINE_SIZE: data.engineSize
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


def calculate_median(column, median_list):
    grouped = get_grouped_data_by_column(column)
    column_list = percentage_value_maps.select_distinct_column(column)
    for item in column_list:
        column_data = grouped.get_group(item)
        calculate_median_per_column_value(column_data, median_list, item)


def get_distinct_values(data_frame, column):
    return data_frame[column].unique().tolist()


def calculate_models_medians():
    brand_list = percentage_value_maps.select_distinct_column(constant.BRAND)
    grouped_by_brand = get_grouped_data_by_column(constant.BRAND)
    for brand in brand_list:
        brand_data = grouped_by_brand.get_group(brand)
        model_list = get_distinct_values(brand_data, constant.BR_MODEL)
        grouped_by_model = brand_data.groupby(constant.BR_MODEL)
        for model in model_list:
            model_data = grouped_by_model.get_group(model)
            calculate_median_per_column_value(model_data, get_model_median_list(brand), model)


def populate_median_lists():
    calculate_median(constant.BRAND, brand_median_list)
    calculate_models_medians()
    calculate_median(constant.TRANSMISSION, transmission_median_list)
    calculate_median(constant.FUEL_TYPE, fuel_type_median_list)
    calculate_median(constant.ENGINE_SIZE, engine_size_median_list)


def fill_all_median_list():
    all_median_list.append({constant.BRAND: brand_median_list})
    all_median_list.append({constant.TRANSMISSION: transmission_median_list})
    all_median_list.append({constant.FUEL_TYPE: fuel_type_median_list})
    all_median_list.append({constant.AUDI: audi_median_list})
    all_median_list.append({constant.BMW: bmw_median_list})
    all_median_list.append({constant.FORD: ford_median_list})
    all_median_list.append({constant.HYUNDI: hyundai_median_list})
    all_median_list.append({constant.MERCEDES: mercedes_median_list})
    all_median_list.append({constant.SKODA: skoda_median_list})
    all_median_list.append({constant.TOYOTA: toyota_median_list})
    all_median_list.append({constant.VAUXHALL: vauxhall_median_list})
    all_median_list.append({constant.VW: vw_median_list})


def print_median_lists():
    print(brand_median_list)
    print(transmission_median_list)
    print(fuel_type_median_list)
    # all_median_list.append({constant.ENGINE_SIZE: engine_size_median_list})
    # print(engine_size_median_list)
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


def calculate_median_percentages_per_list(median_list):
    total = 0
    n = 0
    percentage_list = []
    for item in median_list:
        total += list(item.values())[0]
        n += 1
    for item in median_list:
        percentage_list.append({list(item.keys())[0]: round((list(item.values())[0] / total) * 100, 2)})

    return percentage_list


def convert_list_to_dict(list_to_convert):
    dict = {}
    for item in list_to_convert:
        dict[list(item.keys())[0]] = list(item.values())[0]
    return dict


def calculate_median_percentages():
    for median_list in all_median_list:
        percentage_list = calculate_median_percentages_per_list(list(median_list.values())[0])
        percentage_dict = convert_list_to_dict(percentage_list)
        all_percentage_median_list[list(median_list.keys())[0]] = percentage_dict


def print_median_percentages():
    for percentage_median_list in all_percentage_median_list:
        print(percentage_median_list)


def populate_module_median_percentage_list():
    for median_list in all_percentage_median_list.keys():
        if median_list in modules:
            appended_module_median_list.update(all_percentage_median_list[median_list])


def populate_lists():
    populate_median_lists()
    fill_all_median_list()
    calculate_median_percentages()
    populate_module_median_percentage_list()


def get_median_lists():
    return all_median_list


def get_median_percentage_lists():
    return all_percentage_median_list


def get_median_percentage_list(median_list):
    return all_percentage_median_list[median_list]


def get_module_percentage_list():
    return appended_module_median_list
