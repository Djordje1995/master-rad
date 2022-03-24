import constant
import csv_handler
import percentage_value_maps


def get_file_list():
    return [constant.AUDI,
            constant.FORD,
            constant.BMW,
            constant.HYUNDI,
            constant.MERCEDES,
            constant.SKODA,
            constant.TOYOTA,
            constant.VW,
            constant.VAUXHALL]


def append_file(master, file):
    for row in file:
        master.append(row)
    return master


def init_data(learning_data, testing_data):
    learning_data.append(csv_handler.get_header())
    testing_data.append(csv_handler.get_header())


def transfer_file_data(learning_data, testing_data, file_data):
    header = False
    i = 0
    for row in file_data:
        if not header:
            header = True
            continue
        if i < 2:
            learning_data.append(row)
            i += 1
        else:
            testing_data.append(row)
            i = 0


def create_learning_and_testing_data():
    learning_data = []
    testing_data = []
    init_data(learning_data, testing_data)
    for file in get_file_list():
        file_data = csv_handler.read_csv(file)
        transfer_file_data(learning_data, testing_data, file_data)
    csv_handler.write_csv(learning_data, constant.DATA_FOLDER, constant.LEARNING_DATA)
    csv_handler.write_csv(testing_data, constant.DATA_FOLDER, constant.TESTING_DATA)


def map_brand_to_model(data):
    model = ""
    brand_model_map = {}
    for item in data:
        if item[constant.MODEL] != model:
            model = item[constant.MODEL]
            brand_model_map[model] = item[constant.BRAND]
    return brand_model_map


def print_file(file):
    for item in file:
        print(item)


def remove_difficult_data(file):
    new_file = []
    for row in file:
        if row[constant.TRANSMISSION] != 'Other' and row[constant.FUEL_TYPE] != 'Other':
            new_file.append(row)
    return new_file


def recreate_file(file_name):
    read_file = ''
    write_file = ''
    if file_name == constant.LEARNING:
        read_file = constant.LEARNING
        write_file = constant.LEARNING_DATA
    else:
        read_file = constant.TESTING
        write_file = constant.TESTING_DATA

    file = csv_handler.read_csv(read_file)
    new_file = remove_difficult_data(file)
    csv_handler.write_csv(new_file, write_file)


def recreate_testing_file(file_name):
    file = csv_handler.read_csv(file_name)
    model_lsit = list(percentage_value_maps.get_model_map().keys())
    new_file = []
    header = True
    for row in file:
        if header:
            new_file.append(row)
            header = False
            continue
        if row[constant.MODEL] in model_lsit:
            new_file.append(row)
    csv_handler.write_csv(new_file, constant.TESTING_DATA)

