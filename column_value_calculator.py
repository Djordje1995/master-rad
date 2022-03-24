import constant
import csv_handler
import percentage_value_maps


def find_min_year():
    data = csv_handler.read_csv(constant.LEARNING_DATA)
    oldest_car = 2020
    for row in data:
        if int(row[constant.YEAR]) < oldest_car:
            oldest_car = int(row[constant.YEAR])
    return oldest_car


def find_max_mileage():
    data = csv_handler.read_csv(constant.LEARNING_DATA)
    max_car_mileage = 0
    for row in data:
        if int(row[constant.MILEAGE]) > max_car_mileage:
            max_car_mileage = int(row[constant.YEAR])
    return max_car_mileage


def find_min_max_tax():
    data = csv_handler.read_csv(constant.LEARNING_DATA)
    min_taxes = 200
    max_taxes = 0
    for row in data:
        if int(row[constant.TAX]) > max_taxes:
            max_taxes = int(row[constant.TAX])
        if int(row[constant.TAX]) < min_taxes and int(row[constant.TAX]) != '0':
            min_taxes = int(row[constant.TAX])
    return {'min_tax': min_taxes, 'max_tax': max_taxes}


min_year = find_min_year()
max_mileage = find_max_mileage()
min_max_tax = find_min_max_tax()


def calculate_brand_value(brand):
    return percentage_value_maps.get_brand_map()[brand]


def calculate_model_value(model):
    return percentage_value_maps.get_model_map()[model]


def calculate_year_value(year):
    return (int(year) - min_year) * 0.5 + 0.5


def calculate_transmission_value(transmission):
    return percentage_value_maps.get_transmission_map()[transmission]


def calculate_mileage_value(mileage):
    return (max_mileage - int(mileage)) * 0.05 + 0.05


def calculate_fuel_type_value(fuel_type):
    """hardcoded initial values based on internet research of fuel type"""
    return percentage_value_maps.get_fuel_type_map()[fuel_type]


def calculate_tax_value(tax):
    """first example for road tax value, the higher the tax the lower the buying price"""
    if tax == 0:
        return min_max_tax['max_tax'] / 100 + 5
    else:
        return (min_max_tax['max_tax'] - int(tax)) / 100


def calculate_mpg_value(mpg):
    """more miles per gallon, less the consumption, higher buying price"""
    return float(mpg.replace(',', '.'))


def calculate_engine_size_value(engine_size):
    """higher engine size, higher buying price"""
    return float(engine_size.replace(',', '.'))


def get_calculated_values(column, value):
    switcher = {
        constant.BRAND: calculate_brand_value,
        constant.MODEL: calculate_model_value,
        constant.YEAR: calculate_year_value,
        constant.TRANSMISSION: calculate_transmission_value,
        constant.MILEAGE: calculate_mileage_value,
        constant.FUEL_TYPE: calculate_fuel_type_value,
        constant.TAX: calculate_tax_value,
        constant.MPG: calculate_mpg_value,
        constant.ENGINE_SIZE: calculate_engine_size_value
    }
    calculator = switcher.get(column)
    return calculator(value)
