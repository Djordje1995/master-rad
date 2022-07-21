import csv
import constant
import pandas as pd


header = [
          constant.BRAND,
          constant.BR_MODEL,
          constant.YEAR,
          constant.PRICE,
          constant.TRANSMISSION,
          constant.MILEAGE,
          constant.FUEL_TYPE,
          constant.TAX,
          constant.MPG,
          constant.ENGINE_SIZE
          ]

serbian_headers = ['Marka',
                   'Model',
                   'Godište',
                   'Kilometraža',
                   'Karoserija',
                   'Gorivo',
                   'Kubikaža',
                   'Snaga motora',
                   'Emisiona klasa motora',
                   'Pogon',
                   'Menjač',
                   'Cena']

new_serbian_headers = [
                    'Model',
                    'Godište',
                    'Kilometraža',
                    # 'Karoserija',
                    # 'Gorivo',
                    'Kubikaža',
                    'Snaga motora',
                    # 'Emisiona klasa motora',
                    # 'Pogon',
                    # 'Menjač',
                    'Cena']


def get_header():
    return header


def read_csv(file_name, headers):
    full_data = pd.read_csv(constant.DATA_FOLDER + file_name + constant.CSV)
    headered_data = full_data[headers]
    data = headered_data.T.to_dict()
    return data.values()


learning_data = read_csv(constant.LEARNING_DATA, header)
testing_data = read_csv(constant.TESTING_DATA, header)
learning = read_csv(constant.LEARNING, header)
testing = read_csv(constant.TESTING, header)
learning_data_serbian = read_csv(constant.LEARNING_DATA_SERBIAN, new_serbian_headers)
testing_data_serbian = read_csv(constant.TESTING_DATA_SERBIAN, new_serbian_headers)
full_data_serbian = read_csv(constant.FULL_DATA_SERBIAN, new_serbian_headers)


def get_full_data_serbian():
    return full_data_serbian


def get_learning_data_serbian():
    return learning_data_serbian


def get_testing_data_serbian():
    return testing_data_serbian


def get_learning_data():
    return learning_data


def get_testing_data():
    return testing_data


def get_by_file_name(file_name):
    if file_name == constant.LEARNING:
        return learning
    else:
        return testing


def write_rows(writer, data, header):
    writer.writerow(header)
    is_header = True
    for row in data:
        if is_header:
            is_header = False
            continue
        values = row.values()
        writer.writerow(list(values))


def write_csv(data, file_name, header):
    with open(constant.DATA_FOLDER + file_name + constant.CSV, encoding='utf-8', mode='w', newline='\n') as file:
        writer = csv.writer(file)
        write_rows(writer, data, header)

