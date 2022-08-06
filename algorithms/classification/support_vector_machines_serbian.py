import matplotlib.pyplot as plt
import sklearn.model_selection as model_selection
from sklearn.svm import SVC
from sklearn.metrics import r2_score, confusion_matrix, f1_score, accuracy_score
import seaborn as sns
import pandas as pd
from utils import constant
import time


def visualise_predicted_results(y_test, y_pred):
    plt.figure(figsize=(15, 10))
    plt.scatter(y_test, y_pred)
    plt.xlabel("Actual prices")
    plt.ylabel("Predicted prices")
    plt.title("Actual vs Predicted prices")
    plt.show()


def visualize_confusion_matrix(cm):
    plt.figure(figsize=(7, 7))
    sns.heatmap(cm, annot=True)
    plt.xlabel("Predicted")
    plt.ylabel("Truth")
    plt.show()


def confusion_matrix_display(y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred)
    # visualize_confusion_matrix(cm)
    print(cm)


def print_price_map(data):
    full_data = pd.DataFrame(data)
    prices = full_data[constant.CENA]
    prices.to_numpy().sort()
    for item in prices:
        print(item)
    n_of_classes = 5
    increment = int(len(prices) / 5)
    i = 1
    classes = []
    while i <= n_of_classes:
        item = prices[increment * i - 1]
        i += 1
        print(item)
        classes.append(item)
    return classes


class SVMSerbian:

    def __init__(self, training_data, testing_data, x_train, y_train, x_test, y_test):
        self.training_data = training_data
        self.testing_data = testing_data
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.model_poly = SVC(kernel='poly', degree=3, C=1)
        # self.model_rbf = SVC(kernel='rbf', gamma=0.5, C=0.1)
        self.model_rbf = SVC(kernel='rbf', probability=True, gamma=0.1, C=1)

    def get_model_poly(self):
        return self.model_poly

    def get_model_rbf(self):
        return self.model_rbf

    def train_poly(self):
        start = time.time()
        self.model_poly.fit(self.x_train, self.y_train)
        end = time.time()
        print()
        print("SVM with polynomial kernel:")
        print("Training time: ", end - start, " seconds")
        self.evaluate_test_results_poly()

    def train_rbf(self):
        start = time.time()
        self.model_rbf.fit(self.x_train, self.y_train)
        end = time.time()
        print()
        print("SVM with rbf kernel:")
        print("Training time: ", end - start, " seconds")
        self.evaluate_test_results_rbf()

    def evaluate_test_results_poly(self):
        start = time.time()
        pred = self.model_poly.predict(self.x_test)
        end = time.time()
        print("Testing time: ", end - start, " seconds")
        evaluation = r2_score(self.y_test, pred)
        print("R^2 (coefficient of determination) regression score function: ", evaluation)
        accuracy = accuracy_score(self.y_test, pred)
        f1 = f1_score(self.y_test, pred, average='weighted')
        print('Accuracy: ', "%.2f" % (accuracy * 100))
        print('F1: ', "%.2f" % (f1 * 100))
        confusion_matrix_display(self.y_test, pred)

    def evaluate_test_results_rbf(self):
        start = time.time()
        pred = self.model_rbf.predict(self.x_test)
        end = time.time()
        print("Testing time: ", end - start, " seconds")
        evaluation = r2_score(self.y_test, pred)
        print("R^2 (coefficient of determination) regression score function: ", evaluation)
        accuracy = accuracy_score(self.y_test, pred)
        f1 = f1_score(self.y_test, pred, average='weighted')
        print('Accuracy: ', "%.2f" % (accuracy * 100))
        print('F1: ', "%.2f" % (f1 * 100))
        confusion_matrix_display(self.y_test, pred)
        # visualise_predicted_results(self.y_test, y_pred)
