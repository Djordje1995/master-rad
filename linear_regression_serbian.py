import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import csv_handler
import linear_regression_visualisation
import constant


def calculate_absolute_difference(actual_value, predicted_value):
    if float(actual_value) < predicted_value:
        return predicted_value - float(actual_value)
    return float(actual_value) - predicted_value


def calculate_percentage_difference(actual_value, predicted_value):
    return ((predicted_value - actual_value) / float(actual_value)) * 100


def write_test_predicted_csv(file_name, test_data, y_pred):
    i = 0
    for row in test_data:
        row[constant.PREDIKCIONA_CENA] = round(y_pred[i], 2)
        row[constant.APSOLUTNA_RAZLIKA] = round((y_pred[i] - float(row[constant.CENA])), 2)
        row[constant.PROCENAT] = round(calculate_percentage_difference(float(row[constant.CENA]), y_pred[i]), 2)
        i += 1
    header = csv_handler.serbian_headers
    header.append(constant.PREDIKCIONA_CENA)
    header.append(constant.APSOLUTNA_RAZLIKA)
    header.append(constant.PROCENAT)
    csv_handler.write_csv(test_data, file_name, header)


def evaluate_results(y_test, y_pred):
    evaluation = r2_score(y_test, y_pred)
    print("R^2 (coefficient of determination) regression score function:")
    print(evaluation)
    linear_regression_visualisation.visualise_predicted_results(y_test, y_pred)


def plot_corr(df, size=11):
    corr = df.corr()
    fig, ax = plt.subplots(figsize=(size, size))
    ax.matshow(corr)
    plt.xticks(range(len(corr.columns)), corr.columns)
    plt.yticks(range(len(corr.columns)), corr.columns)


def train(x, y, x_test, y_test):
    # learning_data = csv_handler.get_learning_data_serbian()
    # data_df = pd.DataFrame(learning_data)
    # plot_corr(data_df, 7)
    model = LinearRegression()
    model.fit(x, y)
    y_pred = model.predict(x_test)
    evaluate_results(y_test, y_pred)
    i = 0
    count = 0
    for item in y_pred:
        if item < 0:
            count += 1
            print(str(count) + str(x_test[i]))
        i += 1
    # write_test_predicted_csv(constant.SERBIAN_LINEAR_REGRESSION_RESULT, test_data, y_pred)
