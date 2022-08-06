import constant
import csv_handler
import percentage_value_maps


def find_min_year():
    data = csv_handler.get_learning_data()
    oldest_car = 2020
    for row in data:
        if int(row[constant.YEAR]) < oldest_car:
            oldest_car = int(row[constant.YEAR])
    return oldest_car


def find_max_mileage():
    data = csv_handler.get_learning_data()
    max_car_mileage = 0
    for row in data:
        if int(row[constant.MILEAGE]) > max_car_mileage:
            max_car_mileage = int(row[constant.YEAR])
    return max_car_mileage


def find_min_max_tax():
    data = csv_handler.get_learning_data()
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
    return percentage_value_maps.get_brand_map()[brand] / 100


def calculate_model_value(model):
    return percentage_value_maps.get_model_map()[model] / 100


def calculate_year_value(year):
    """Median value was used (2017), min = 2002"""
    # return (int(year) - min_year) * 0.5 + 0.5
    return int(year) - 2002 + 1


def calculate_transmission_value(transmission):
    return percentage_value_maps.get_transmission_map()[transmission] / 100


def calculate_mileage_value(mileage):
    """The median value was used (19170), avg (24438)"""
    """maximum is 149958.0, this is used so that the value is always positive"""
    return (149958 - int(mileage) + 100) / 1000


def calculate_fuel_type_value(fuel_type):
    return percentage_value_maps.get_fuel_type_map()[fuel_type] / 100


def calculate_tax_value(tax):
    """first example for road tax value, the higher the tax the lower the buying price"""
    if tax == 0:
        return min_max_tax['max_tax'] / 100 + 5
    else:
        return (min_max_tax['max_tax'] - int(tax)) / 100


def calculate_mpg_value(mpg):
    """55 mpg is avg(median)"""
    """more miles per gallon, less the consumption, higher buying price"""
    """minimum is 20.8, this is used so that the value is always positive"""
    return (mpg - 20.8) + 5


def calculate_engine_size_value(engine_size):
    """higher engine size, higher buying price"""
    """1.6 is median for engine_size, and 1.0 is a minimum, this is used so that the value is always positive"""
    return (engine_size - 1.0) + 0.3


def get_calculated_values(column, value):
    switcher = {
        constant.BRAND: calculate_brand_value,
        constant.BR_MODEL: calculate_model_value,
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
