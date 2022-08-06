import numpy as np

from algorithms.classification.multinomial_logistic_regression import MultinomialLogisticRegressionSerbian
from utils import column_value_calculator_serbian
from utils import constant
from utils import csv_handler
from utils import median_calculator_serbian
from algorithms.regression.linear_regression_serbian import LinearRegressionSerbian
from algorithms.regression.polynomial_regression_serbian import PolynomialRegressionSerbian
from algorithms.regression.lasso_regression_serbian import LassoRegressionSerbian
from algorithms.regression.ridge_regression_serbian import RidgeRegressionSerbian
from algorithms.classification.naive_bayes_serbian import NaiveBayesSerbian
from algorithms.classification.support_vector_machines_serbian import SVMSerbian
from algorithms.classification.knn_serbian import KNNSerbian


median_calculator_serbian.populate_lists()

classification_algorithms = [
            'Naive bayes',
            'Support vector machine polynomial',
            'Support vector machine rbf',
            'K Nearest neighbours euclidean',
            'K Nearest neighbours manhattan',
            'K Nearest neighbours chebyshev',
            'K Nearest neighbours minkowski',
            'K Nearest neighbours cosine'
]

y_data_map = {constant.MANJE_OD_2000: 0,
              constant.IZMEDJU_2000_I_5000: 1,
              constant.IZMEDJU_5000_I_10000: 2,
              constant.IZMEDJU_10000_I_15000: 3,
              constant.PREKO_15000: 4}

reverse_y_data_map = {0: constant.MANJE_OD_2000,
                      1: constant.IZMEDJU_2000_I_5000,
                      2: constant.IZMEDJU_5000_I_10000,
                      3: constant.IZMEDJU_10000_I_15000,
                      4: constant.PREKO_15000}


def get_y_data(price):
    if price < 2000:
        return y_data_map[constant.MANJE_OD_2000]
    elif 2000 <= price < 5000:
        return y_data_map[constant.IZMEDJU_2000_I_5000]
    elif 5000 <= price < 10000:
        return y_data_map[constant.IZMEDJU_5000_I_10000]
    elif 10000 <= price < 15000:
        return y_data_map[constant.IZMEDJU_10000_I_15000]
    else:
        return y_data_map[constant.PREKO_15000]


def fill_data(row, x, y, y_class):
    """ fills the corresponding x and y matrix for linear regression"""
    temp = []
    for item in row:
        if item in csv_handler.new_serbian_headers:
            if item == constant.CENA:
                y.append(int(row[item]))
                y_class.append(get_y_data(int(row[item])))
            else:
                temp.append(column_value_calculator_serbian.get_calculated_values(item, row[item]))
    x.append(temp)


def convert_values_to_predict(form_data, x):
    for item in form_data:
        x.append(column_value_calculator_serbian.get_calculated_values(item, form_data[item]))


class Algorithms:
    def __init__(self):
        # models
        self.linear_regression_model = {}
        self.polynomial_regression_model = {}
        self.lasso_regression_model = {}
        self.ridge_regression_model = {}
        # self.multinomial_logistic_regression_model = {}
        self.naive_bayes_model = {}
        self.svm_model_poly = {}
        self.svm_model_rbf = {}
        self.knn_model = {}

    def get_model(self, algorithm):
        switcher = {
            'Linear regression': self.linear_regression_model.get_model(),
            'Polynomial regression': self.polynomial_regression_model.get_model(),
            'Lasso regression': self.lasso_regression_model.get_model(),
            'Ridge regression': self.ridge_regression_model.get_model(),
            # 'Multinomial logistic regression': self.multinomial_logistic_regression_model
            'Naive bayes': self.naive_bayes_model.get_model(),
            'Support vector machine polynomial': self.svm_model_poly.get_model_poly(),
            'Support vector machine rbf': self.svm_model_rbf.get_model_rbf(),
            'K Nearest neighbours euclidean': self.knn_model.get_model("euclidean"),
            'K Nearest neighbours manhattan': self.knn_model.get_model("manhattan"),
            'K Nearest neighbours chebyshev': self.knn_model.get_model("chebyshev"),
            'K Nearest neighbours minkowski': self.knn_model.get_model("minkowski"),
            'K Nearest neighbours cosine': self.knn_model.get_model("cosine")
        }
        return switcher[algorithm]

    def predict(self, form_data, algorithm):
        model = self.get_model(algorithm)
        x = []
        convert_values_to_predict(form_data, x)
        x_test = np.array([x])
        y_pred = model.predict(x_test)
        if algorithm in classification_algorithms:
            return reverse_y_data_map[round(y_pred.reshape(-1, 1)[0][0])]
        return str(round(y_pred.reshape(-1, 1)[0][0]))

    def train_all_algorithms(self):
        training_data = csv_handler.get_learning_data_serbian()
        testing_data = csv_handler.get_testing_data_serbian()
        x_train = []
        y_train = []
        x_test = []
        y_test = []
        y_train_class = []
        y_test_class = []
        for row in training_data:
            fill_data(row, x_train, y_train, y_train_class)
        for row in testing_data:
            fill_data(row, x_test, y_test, y_test_class)

        # linear regression model training
        self.linear_regression_model = LinearRegressionSerbian(training_data, testing_data, x_train, y_train, x_test, y_test)
        self.linear_regression_model.train()

        self.polynomial_regression_model = PolynomialRegressionSerbian(training_data, testing_data, x_train, y_train, x_test, y_test)
        self.polynomial_regression_model.train()

        self.lasso_regression_model = LassoRegressionSerbian(training_data, testing_data, x_train, y_train, x_test, y_test)
        self.lasso_regression_model.train()

        self.ridge_regression_model = RidgeRegressionSerbian(training_data, testing_data, x_train, y_train, x_test, y_test)
        self.ridge_regression_model.train()

        # self.multinomial_logistic_regression_model = MultinomialLogisticRegressionSerbian(training_data, testing_data, x_train, y_train_class, x_test, y_test_class)
        # self.multinomial_logistic_regression_model.train()

        self.naive_bayes_model = NaiveBayesSerbian(training_data, testing_data, x_train, y_train_class, x_test, y_test_class)
        self.naive_bayes_model.train()

        self.svm_model_rbf = SVMSerbian(training_data, testing_data, x_train, y_train_class, x_test, y_test_class)
        self.svm_model_poly = self.svm_model_rbf
        self.svm_model_poly.train_poly()
        # self.svm_model_rbf.train_rbf()

        self.knn_model = KNNSerbian(training_data, testing_data, x_train, y_train_class, x_test, y_test_class)
        self.knn_model.train("euclidean")
        self.knn_model.train("manhattan")
        self.knn_model.train("chebyshev")
        self.knn_model.train("minkowski")
        self.knn_model.train("cosine")

