import constant
import csv_handler
import median_calculator

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


def sort_category_by_value(category_dict):
    sorted_list = list(category_dict.keys())
    sorted_list.sort()
    sorted_dict = {}
    for key in sorted_list:
        sorted_dict[key] = category_dict[key]
    return sorted_dict


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


def select_distinct_column(column_name):
    data = csv_handler.get_learning_data()
    distinct_column_list = []
    for row in data:
        if row[column_name] not in distinct_column_list:
            distinct_column_list.append(row[column_name])
    return distinct_column_list


def select_distinct_column_from_data(data, column_name):
    distinct_column_list = []
    for row in data:
        if row[column_name] not in distinct_column_list:
            distinct_column_list.append(row[column_name])
    return distinct_column_list


def get_transmission_map():
    return median_calculator.get_median_percentage_list(constant.TRANSMISSION)


def get_fuel_type_map():
    return median_calculator.get_median_percentage_list(constant.FUEL_TYPE)


def get_brand_map():
    return median_calculator.get_median_percentage_list(constant.BRAND)


def get_model_map():
    return median_calculator.get_module_percentage_list()
