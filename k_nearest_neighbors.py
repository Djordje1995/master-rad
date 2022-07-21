import column_value_calculator
import constant
import csv_handler
import math
import pandas as pd
import knn_visualisation
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import time
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint


def y_data_map():
    return {constant.LESS_THEN_9000: 0,
            constant.BETWEEN_9000_AND_12000: 1,
            constant.BETWEEN_12000_AND_16000: 2,
            constant.BETWEEN_16000_AND_21000: 3,
            constant.MORE_THEN_21000: 4}


def reverse_y_data_map():
    return {0: constant.LESS_THEN_9000,
            1: constant.BETWEEN_9000_AND_12000,
            2: constant.BETWEEN_12000_AND_16000,
            3: constant.BETWEEN_16000_AND_21000,
            4: constant.MORE_THEN_21000}


def get_y_data(row):
    if float(row[constant.PRICE]) < 9000:
        return y_data_map()[constant.LESS_THEN_9000]
    elif 9000 <= float(row[constant.PRICE]) < 12000:
        return y_data_map()[constant.BETWEEN_9000_AND_12000]
    elif 12000 <= float(row[constant.PRICE]) < 16000:
        return y_data_map()[constant.BETWEEN_12000_AND_16000]
    elif 16000 <= float(row[constant.PRICE]) < 21000:
        return y_data_map()[constant.BETWEEN_16000_AND_21000]
    else:
        return y_data_map()[constant.MORE_THEN_21000]


def get_x_data(row):
    return [column_value_calculator.calculate_brand_value(row[constant.BRAND]),
            column_value_calculator.calculate_model_value(row[constant.BR_MODEL]),
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


def prepare_out_data(x_data, y_pred, y_test):
    """add real and predicted stringified number"""
    i = 0
    out_data = []
    miss = 0
    match = 0
    while i < len(x_data):
        out_row = x_data[i]
        out_row[constant.KNN_VALUE] = y_pred[i]
        out_row[constant.PREDICTED_PRICE] = reverse_y_data_map()[y_pred[i]]
        out_row[constant.MISS_MATCH] = "Match" if y_pred[i] == y_test[i] else "Miss"
        if y_pred[i] == y_test[i]:
            match += 1
        else:
            miss += 1
        out_data.append(out_row)
        i += 1
    print("Missed: " + str(miss))
    print("Matched: " + str(match))
    return out_data


def create_price_map():
    full_data = pd.read_csv(constant.DATA_FOLDER + constant.LEARNING_DATA + constant.CSV)
    prices = full_data[constant.PRICE]
    prices.to_numpy().sort()
    i = 0
    for row in prices:
        if i == int(len(prices) / 5):
            print(row)
            i = 0
        i += 1


def score(knn_model, x_test, y_test):
    print("KNN Score: ")
    print(knn_model.score(x_test, y_test))


def confusion_matrix_display(y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred)
    knn_visualisation.visualize_confusion_matrix(cm)
    print(cm)


def print_classification_report(y_test, y_pred):
    print(classification_report(y_test, y_pred))


def visualise(knn_model, x_test, y_test):
    plot_confusion_matrix(knn_model,
                          x_test,
                          y_test,
                          cmap='Blues')
    plt.show()


def count_different_classes(data):
    counts = []
    df = pd.DataFrame(data)
    prices = df[constant.PRICE]
    sorted = prices.sort_values().tolist()
    i = 4
    while i < 10:
        j = 1
        while j <= i:
            counts.append(sorted[int((j * len(sorted)) / i) - 1])
            j += 1
        print(counts)
        counts = []
        i += 1


def train_one(metric, params, x_train, y_train, x_test, y_test, test_data):
    print("Metric used: " + metric)

    k = round(math.sqrt(len(x_train)))
    print(k)

    # stard measuring time
    start = time.time()

    knn_model = KNeighborsClassifier(n_neighbors=k,
                                     metric=metric,
                                     metric_params=params,
                                     algorithm='auto',
                                     n_jobs=1)
    # knn_model = KNeighborsClassifier(n_neighbors=k)
    # napraviti komparaciju sa cosine similarity metrikom i bez nje, videti koje sve mogu algoritmi i n_jobs da budu
    # pa tu komparaciju iskoristiti za nesto za master
    knn_model.fit(x_train, y_train)
    y_data_pred = knn_model.predict(x_train)
    visualise(knn_model, x_train, y_train)
    # visualise(knn_model, x_test, y_test)

    score(knn_model, x_test, y_test)

    y_pred = knn_model.predict(x_test)
    print(set(y_test) - set(y_pred))
    print_classification_report(y_test, y_pred)

    # finish measuring time
    prepare_out_data(list(test_data), y_pred, y_test)
    end = time.time()
    print("Time in seconds: " + str(end - start))


def train():
    data = csv_handler.get_learning_data()
    create_price_map()
    x_train, y_train = create_data(data)

    test_data = csv_handler.get_testing_data()
    x_test, y_test = create_data(test_data)

    # scaler = StandardScaler()
    # x_train = scaler.fit_transform(x_train)
    # x_test = scaler.transform(x_test)

    # classifier = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=50)
    # classifier.fit(x_train, y_train)

    # est = RandomForestClassifier(n_jobs=-1)
    # rf_p_dist = {'max_depth': [3, 5, 10, None],
    #              'n_estimators': [100, 200, 300, 400, 500],
    #              'max_features': randint(1, 9),
    #              'criterion': ['gini', 'entropy'],
    #              'bootstrap': [True, False],
    #              'min_samples_leaf': randint(1, 4)}  # videti sta je ovo min sample leaf

    # t = time.time()
    # print("started at:")
    # print(t)
    # rdmsearch = RandomizedSearchCV(est, param_distributions=rf_p_dist, n_jobs=-1, n_iter=40, cv=9)
    # rdmsearch.fit(x_train, y_train)
    # print("kolko je trajalo:")
    # print(time.time() - t)
    # ht_params = rdmsearch.best_params_
    # ht_score = rdmsearch.best_score_
    # print(ht_params)
    # print(ht_score)
    #
    # y_pred = classifier.predict(x_test)
    # cm = confusion_matrix(y_test, y_pred)
    # print(cm)
    # print(y_pred)
    # scoreics = accuracy_score(y_test, y_pred)
    # print(scoreics)

    train_one('euclidean', None, x_train, y_train, x_test, y_test, test_data)
    train_one('manhattan', None, x_train, y_train, x_test, y_test, test_data)
    train_one('chebyshev', None, x_train, y_train, x_test, y_test, test_data)
    train_one('minkowski', None, x_train, y_train, x_test, y_test, test_data)
    train_one('cosine', None, x_train, y_train, x_test, y_test, test_data)

    # y_pred_formatted = round_knn_results(y_pred)
    # header = csv_handler.get_header()
    # header.append(constant.KNN_VALUE)
    # header.append(constant.PREDICTED_PRICE)
    # header.append(constant.MISS_MATCH)
    # csv_handler.write_csv(prepare_out_data(list(test_data), y_pred, y_test), constant.KNN_RESULT, header)
