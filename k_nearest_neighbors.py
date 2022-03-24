import column_value_calculator
import constant
import csv_handler
from sklearn.neighbors import KNeighborsRegressor


def y_data_map():
    return {constant.LESS_THEN_5000: 0,
            constant.BETWEEN_5000_AND_7500: 1,
            constant.BETWEEN_7500_AND_10000: 2,
            constant.BETWEEN_10000_AND_12500: 3,
            constant.BETWEEN_12500_AND_15000: 4,
            constant.BETWEEN_15000_AND_17500: 5,
            constant.BETWEEN_17500_AND_20000: 6,
            constant.BETWEEN_20000_AND_25000: 7,
            constant.BETWEEN_25000_AND_30000: 8,
            constant.MORE_THEN_30000: 9}


def get_y_data(row):
    if float(row[constant.PRICE]) < 5000:
        return y_data_map()[constant.LESS_THEN_5000]
    elif 5000 <= float(row[constant.PRICE]) < 7500:
        return y_data_map()[constant.BETWEEN_5000_AND_7500]
    elif 7500 <= float(row[constant.PRICE]) < 10000:
        return y_data_map()[constant.BETWEEN_7500_AND_10000]
    elif 10000 <= float(row[constant.PRICE]) < 12500:
        return y_data_map()[constant.BETWEEN_10000_AND_12500]
    elif 12500 <= float(row[constant.PRICE]) < 15000:
        return y_data_map()[constant.BETWEEN_12500_AND_15000]
    elif 15000 <= float(row[constant.PRICE]) < 17500:
        return y_data_map()[constant.BETWEEN_15000_AND_17500]
    elif 17500 <= float(row[constant.PRICE]) < 20000:
        return y_data_map()[constant.BETWEEN_17500_AND_20000]
    elif 20000 <= float(row[constant.PRICE]) < 25000:
        return y_data_map()[constant.BETWEEN_20000_AND_25000]
    elif 25000 <= float(row[constant.PRICE]) < 30000:
        return y_data_map()[constant.BETWEEN_25000_AND_30000]
    else:
        return y_data_map()[constant.MORE_THEN_30000]


def get_x_data(row):
    return [column_value_calculator.calculate_brand_value(row[constant.BRAND]),
            column_value_calculator.calculate_model_value(row[constant.MODEL]),
            column_value_calculator.calculate_year_value(row[constant.YEAR]),
            column_value_calculator.calculate_transmission_value(row[constant.TRANSMISSION]),
            column_value_calculator.calculate_mileage_value(row[constant.MILEAGE]),
            column_value_calculator.calculate_fuel_type_value(row[constant.FUEL_TYPE]),
            column_value_calculator.calculate_tax_value(row[constant.TAX]),
            column_value_calculator.calculate_mpg_value(row[constant.MPG]),
            column_value_calculator.calculate_engine_size_value(row[constant.ENGINE_SIZE])]


def create_data(data):
    x_data = []
    y_data = []
    for row in data:
        x_data.append(get_x_data(row))
        y_data.append(get_y_data(row))
    return x_data, y_data


def prepare_out_data(x_data, y_pred):
    """add real and predicted stringified number"""
    i = 0
    out_data = []
    while i < x_data.__len__():
        out_row = x_data[i]
        out_row[constant.PREDICTED_PRICE] = y_pred[i]
        out_data.append(out_row)
        i += 1
    return out_data


def round_knn_results(y_pred):
    i = 0
    while i < y_pred.__len__():
        y_pred[i] = round(y_pred[i])
        i += 1
    return y_pred


def train():
    data = csv_handler.read_csv(constant.LEARNING_DATA)
    x_data, y_data = create_data(data)
    knn_model = KNeighborsRegressor(n_neighbors=5)
    knn_model.fit(x_data, y_data)
    test_data = csv_handler.read_csv(constant.TESTING_DATA)
    x_test, y_test = create_data(test_data)
    y_pred = knn_model.predict(x_test)
    y_pred_formatted = round_knn_results(y_pred)
    header = csv_handler.get_header()
    header.append(constant.KNN_VALUE)
    header.append(constant.PREDICTED_PRICE)
    csv_handler.write_csv(prepare_out_data(test_data, y_pred_formatted), constant.KNN_RESULT, header)
