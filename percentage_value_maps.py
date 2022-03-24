import constant
import csv_handler


TOTAL = 'total'
COUNT = 'count'
AVG = 'avg'


def calculate_percentage_per_item(total, value):
    return (value / total) * 100


def calculate_differences_in_percentage(category_dict):
    total = 0
    count = 0
    percentage_dict = {}
    for item in category_dict:
        total += category_dict[item][AVG]
        count += 1
    for item in category_dict:
        percentage_dict[item] = calculate_percentage_per_item(total, category_dict[item][AVG])
    return percentage_dict


def print_avgs(category_dict):
    for key in category_dict:
        print(key)
        print(category_dict[key])


def avg_price_per_category(data, category):
    category_dict = {}
    for row in data:
        if row[category] not in category_dict:
            temp = {TOTAL: int(row[constant.PRICE]), COUNT: 1, AVG: int(row[constant.PRICE])}
            category_dict[row[category]] = temp
        else:
            existing = category_dict[row[category]]
            existing[TOTAL] += int(row[constant.PRICE])
            existing[COUNT] += 1
            existing[AVG] = existing[TOTAL] / existing[COUNT]
            category_dict[row[category]] = existing
    return category_dict


def select_distinct_column(file_name, column_name):
    data = csv_handler.read_csv(file_name)
    distinct_column_list = []
    for row in data:
        if row[column_name] not in distinct_column_list:
            distinct_column_list.append(row[column_name])
    return distinct_column_list


def calculate_transmission_map():
    """hardcoded values for different transmission types"""
    return {'Manual': 10, 'Automatic': 20, 'Semi-Auto': 25}


def calculate_fuel_type_map():
    """hardcoded values for different fuel types"""
    return {'Petrol': 10, 'Diesel': 14, 'Hybrid': 20, 'Electric': 24}


transmission_map = calculate_transmission_map()
fuel_type_map = calculate_fuel_type_map()
brand_map = calculate_differences_in_percentage(
    avg_price_per_category(csv_handler.read_csv(constant.LEARNING_DATA), constant.BRAND))
model_map = calculate_differences_in_percentage(
    avg_price_per_category(csv_handler.read_csv(constant.LEARNING_DATA), constant.MODEL))


def get_transmission_map():
    return transmission_map


def get_fuel_type_map():
    return fuel_type_map


def get_brand_map():
    return brand_map


def get_model_map():
    return model_map
