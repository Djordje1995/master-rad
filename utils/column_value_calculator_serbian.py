from utils import constant, median_calculator_serbian, csv_handler


def find_min_year():
    data = csv_handler.get_learning_data_serbian()
    oldest_car = 2020
    for row in data:
        if int(row[constant.GODISTE]) < oldest_car:
            oldest_car = int(row[constant.GODISTE])
    return oldest_car


def find_max_mileage():
    data = csv_handler.get_learning_data_serbian()
    max_car_mileage = 0
    for row in data:
        if int(row[constant.KILOMETRAZA]) > max_car_mileage:
            max_car_mileage = int(row[constant.KILOMETRAZA])
    return max_car_mileage


min_year = find_min_year()
max_mileage = find_max_mileage()


def calculate_model_value(model):
    return median_calculator_serbian.get_median_list(constant.MODEL)[model] / 100


def calculate_year_value(year):
    return int(year) - min_year + 1


def calculate_mileage_value(mileage):
    return (max_mileage - int(mileage) + 100) / 1000


def calculate_car_body_value(car_body):
    return median_calculator_serbian.get_median_list(constant.KAROSERIJA)[car_body] / 100


def calculate_fuel_type_value(fuel_type):
    return median_calculator_serbian.get_median_list(constant.GORIVO)[fuel_type] / 100


def calculate_engine_size_value(engine_size):
    return int(engine_size) / 100


def calculate_engine_power_value(engine_power):
    return int(engine_power)


def calculate_emission_class_value(emission_class):
    return median_calculator_serbian.get_median_list(constant.EMISIONA_KLASA_MOTORA)[emission_class] / 100


def calculate_drive_value(drive):
    return median_calculator_serbian.get_median_list(constant.POGON)[drive] / 100


def calculate_transmission_value(transmission):
    return median_calculator_serbian.get_median_list(constant.MENJAC)[transmission] / 100


def get_calculated_values(column, value):
    switcher = {
        constant.MODEL: calculate_model_value,
        constant.GODISTE: calculate_year_value,
        constant.KILOMETRAZA: calculate_mileage_value,
        constant.KAROSERIJA: calculate_car_body_value,
        constant.GORIVO: calculate_fuel_type_value,
        constant.KUBIKAZA: calculate_engine_size_value,
        constant.SNAGA_MOTORA: calculate_engine_power_value,
        constant.EMISIONA_KLASA_MOTORA: calculate_emission_class_value,
        constant.POGON: calculate_drive_value,
        constant.MENJAC: calculate_transmission_value
    }
    calculator = switcher.get(column)
    return calculator(value)
