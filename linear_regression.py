import constant
import column_value_calculator
from sklearn.linear_model import LinearRegression
import csv_handler


def fill_data(row, x, y):
    temp = []
    for item in row:
        if item == constant.PRICE:
            y.append(int(row[item]))
        else:
            temp.append(column_value_calculator.get_calculated_values(item, row[item]))
    x.append(temp)


def fill_x_data(row, x_pred):
    temp = []
    for item in row:
        if item != constant.PRICE:
            temp.append(column_value_calculator.get_calculated_values(item, row[item]))
    x_pred.append(temp)


def print_item(index, x_item, y_item, test_price):
    print("{}.".format(index))
    for item in x_item:
        print("{}: {}".format(item, x_item[item]))
    print("Real price: {}".format(test_price))
    print("Predicted price: {}".format(y_item))
    difference = float(test_price) - float(y_item)
    print("Difference: {}\n".format(difference))


def print_and_compare(y_pred, test_data):
    i = 0
    while i < len(y_pred):
        print_item(i, test_data[i], y_pred[i], test_data[i][constant.PRICE])
        i += 1


def calculate_absolute_difference(actual_value, predicted_value):
    if float(actual_value) < predicted_value:
        return predicted_value - float(actual_value)
    return float(actual_value) - predicted_value


def calculate_percentage_difference(actual_value, predicted_value):
    return (calculate_absolute_difference(actual_value, predicted_value) / float(actual_value)) * 100


def write_test_predicted_csv(file_name, test_data, y_pred):
    i = 0
    while i < test_data.__len__():
        test_data[i][constant.PREDICTED_PRICE] = round(y_pred[i], 2)
        test_data[i][constant.ABSOLUTE_DIFFERENCE] = round(calculate_absolute_difference(test_data[i][constant.PRICE], y_pred[i]), 2)
        test_data[i][constant.PERCENTAGE] = round(calculate_percentage_difference(test_data[i][constant.PRICE], y_pred[i]), 2)
        i += 1
    header = csv_handler.get_header()
    header.append(constant.PREDICTED_PRICE)
    header.append(constant.ABSOLUTE_DIFFERENCE)
    header.append(constant.PERCENTAGE)
    csv_handler.write_csv(test_data, file_name, header)


def train(data):
    x = []
    y = []
    for row in data:
        fill_data(row, x, y)
    model = LinearRegression()
    model.fit(x, y)
    test_data = csv_handler.read_csv(constant.TESTING_DATA)
    x_pred = []
    for row in test_data:
        fill_x_data(row, x_pred)
    y_pred = model.predict(x_pred)
    write_test_predicted_csv(constant.LINEAR_REGRESSION_RESULT, test_data, y_pred)
    # print_and_compare(y_pred, test_data)
