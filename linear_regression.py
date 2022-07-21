import constant
import column_value_calculator
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import csv_handler
import linear_regression_visualisation


def fill_data(row, x, y):
    """ fills the corresponding x and y matrix for linear regression"""
    temp = []
    for item in row:
        if item in csv_handler.get_header():
            if item == constant.PRICE:
                y.append(int(row[item]))
            else:
                temp.append(column_value_calculator.get_calculated_values(item, row[item]))
    x.append(temp)


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
    return ((predicted_value - actual_value) / float(actual_value)) * 100


def write_test_predicted_csv(file_name, test_data, y_pred):
    i = 0
    for row in test_data:
        row[constant.PREDICTED_PRICE] = round(y_pred[i], 2)
        row[constant.ABSOLUTE_DIFFERENCE] = round((y_pred[i] - float(row[constant.PRICE])), 2)
        row[constant.PERCENTAGE] = round(calculate_percentage_difference(float(row[constant.PRICE]), y_pred[i]), 2)
        i += 1
    header = csv_handler.get_header()
    header.append(constant.PREDICTED_PRICE)
    header.append(constant.ABSOLUTE_DIFFERENCE)
    header.append(constant.PERCENTAGE)
    csv_handler.write_csv(test_data, file_name, header)


def evaluate_results(y_test, y_pred):
    evaluation = r2_score(y_test, y_pred)
    print("R^2 (coefficient of determination) regression score function:")
    print(evaluation)
    linear_regression_visualisation.visualise_predicted_results(y_test, y_pred)


def train(data):
    x = []
    y = []
    for row in data:
        fill_data(row, x, y)
    model = LinearRegression()
    model.fit(x, y)
    test_data = csv_handler.get_testing_data()
    x_test = []
    y_test = []
    for row in test_data:
        fill_data(row, x_test, y_test)
    y_pred = model.predict(x_test)
    count = 0
    i = 0
    for value in y_pred:
        if value < 0:
            count += 1
            print(list(test_data)[i])
            print(value)
        i += 1
    print(count)
    evaluate_results(y_test, y_pred)
    write_test_predicted_csv(constant.LINEAR_REGRESSION_RESULT, test_data, y_pred)
    # print_and_compare(y_pred, test_data)
