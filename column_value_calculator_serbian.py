import median_calculator_serbian
import percentage_value_maps_serbian
import csv_handler

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


def find_min_year():
    data = csv_handler.get_learning_data_serbian()
    oldest_car = 2020
    for row in data:
        if int(row[GODISTE]) < oldest_car:
            oldest_car = int(row[GODISTE])
    return oldest_car


def find_max_mileage():
    data = csv_handler.get_learning_data_serbian()
    max_car_mileage = 0
    for row in data:
        if int(row[KILOMETRAZA]) > max_car_mileage:
            max_car_mileage = int(row[KILOMETRAZA])
    return max_car_mileage


min_year = find_min_year()
max_mileage = find_max_mileage()


def calculate_brand_value(brand):
    return median_calculator_serbian.get_median_list(MARKA)[brand] / 100


def calculate_model_value(model):
    return median_calculator_serbian.get_median_list(MODEL)[model] / 100


def calculate_year_value(year):
    return int(year) - min_year + 1


def calculate_mileage_value(mileage):
    return (max_mileage - int(mileage) + 100) / 1000


def calculate_car_body_value(car_body):
    return median_calculator_serbian.get_median_list(KAROSERIJA)[car_body] / 100


def calculate_fuel_type_value(fuel_type):
    return median_calculator_serbian.get_median_list(GORIVO)[fuel_type] / 100


def calculate_engine_size_value(engine_size):
    return int(engine_size) / 100


def calculate_engine_power_value(engine_power):
    return int(engine_power)


def calculate_emission_class_value(emission_class):
    return median_calculator_serbian.get_median_list(EMISIONA_KLASA_MOTORA)[emission_class] / 100


def calculate_drive_value(drive):
    return median_calculator_serbian.get_median_list(POGON)[drive] / 100


def calculate_transmission_value(transmission):
    return median_calculator_serbian.get_median_list(MENJAC)[transmission] / 100


def get_calculated_values(column, value):
    switcher = {
        'Marka': calculate_brand_value,
        'Model': calculate_model_value,
        'Godište': calculate_year_value,
        'Kilometraža': calculate_mileage_value,
        'Karoserija': calculate_car_body_value,
        'Gorivo': calculate_fuel_type_value,
        'Kubikaža': calculate_engine_size_value,
        'Snaga motora': calculate_engine_power_value,
        'Emisiona klasa motora': calculate_emission_class_value,
        'Pogon': calculate_drive_value,
        'Menjač': calculate_transmission_value
    }
    calculator = switcher.get(column)
    return calculator(value)
