import pandas as pd

import column_value_calculator
import column_value_calculator_serbian
import constant
import csv_handler
import median_calculator
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

import median_calculator_serbian

learning_data = csv_handler.get_learning_data()
testing_data = csv_handler.get_testing_data()
median_calculator.populate_lists()
training_header = [
    constant.BRAND,
    constant.MODEL,
    constant.YEAR,
    constant.TRANSMISSION,
    constant.MILEAGE,
    constant.FUEL_TYPE,
    constant.TAX,
    constant.MPG,
    constant.ENGINE_SIZE]
y_header = [constant.PRICE]

learning_data_serbian = csv_handler.get_learning_data_serbian()
testing_data_serbian = csv_handler.get_testing_data_serbian()
median_calculator_serbian.populate_lists()
serbian_headers = [
                   # 'Marka',
                   'Model',
                   'Godište',
                   'Kilometraža',
                   # 'Karoserija',
                   # 'Gorivo',
                   'Kubikaža',
                   'Snaga motora',
                   # 'Emisiona klasa motora',
                   # 'Pogon',
                   # 'Menjač'
                   ]
y_header_serbian = ['Cena']


def fill_data(row, x, y):
    temp = {}
    for item in row:
        if item in training_header:
            temp[item] = column_value_calculator.get_calculated_values(item, row[item])
        else:
            y.append({item: int(row[item])})
    x.append(temp)


def fill_data_serbian(row, x, y):
    temp = {}
    for item in row:
        if item in serbian_headers:
            temp[item] = column_value_calculator_serbian.get_calculated_values(item, row[item])
        else:
            y.append({item: int(row[item])})
    x.append(temp)


def print_importance(importance):
    i = 0
    for item in serbian_headers:
        print(item + ": " + str(importance[i] * 100))
        i += 1


def check_for_irrelevance(data):
    x = []
    y = []
    for row in data:
        fill_data_serbian(row, x, y)
    xd = pd.DataFrame(x)
    yd = pd.DataFrame(y)

    ###################################################

    test = SelectKBest(score_func=chi2, k=3)
    fit = test.fit(xd, yd)

    np.set_printoptions(precision=3)
    print(fit.scores_)

    features = fit.transform(xd)
    print(features[0:3, :])

    print("AJ SAD")

    model = ExtraTreesClassifier(n_estimators=10)
    model.fit(xd, yd)
    print_importance(model.feature_importances_)

    ####################################################

    model = LogisticRegression()
    rfe = RFE(model, 6)
    fit = rfe.fit(xd, yd.values.ravel())
    print("Num Features: %s" % fit.n_features_)
    print("Selected Features: %s" % fit.support_)
    print("Feature Ranking: %s" % fit.ranking_)


check_for_irrelevance(learning_data_serbian)

