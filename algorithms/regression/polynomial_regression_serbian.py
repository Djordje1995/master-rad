from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import numpy as np
import time


def visualise_predicted_results(y_test, y_pred):
    plt.figure(figsize=(15, 10))
    plt.scatter(y_test, y_pred)
    plt.xlabel("Actual prices")
    plt.ylabel("Predicted prices")
    plt.title("Actual vs Predicted prices")
    plt.show()


class PolynomialRegressionSerbian:

    def __init__(self, training_data, testing_data, x_train, y_train, x_test, y_test):
        self.training_data = training_data
        self.testing_data = testing_data
        self.x_train = np.array(x_train).reshape(-1, 5)
        self.y_train = np.array(y_train).reshape(-1, 1)
        self.x_test = np.array(x_test).reshape(-1, 5)
        self.y_test = np.array(y_test).reshape(-1, 1)
        self.degree = 3
        self.model = make_pipeline(PolynomialFeatures(self.degree), LinearRegression())

    def get_model(self):
        return self.model

    def train(self):
        start = time.time()
        self.model.fit(self.x_train, self.y_train)
        end = time.time()
        print()
        print("Polynomial regression " + str(self.degree) + ":")
        print("Training time: ", end - start, " seconds")
        self.evaluate_test_results()

    def evaluate_test_results(self):
        start = time.time()
        y_pred = self.model.predict(self.x_test)
        end = time.time()
        print("Testing time: ", end - start, " seconds")
        evaluation = r2_score(self.y_test, y_pred)
        print("R^2 (coefficient of determination) regression score function: ", evaluation)
        # visualise_predicted_results(self.y_test, y_pred)
