import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import time


def plot_corr(df, size=11):
    """moram da se setim cemu ovo sluzi"""
    corr = df.corr()
    fig, ax = plt.subplots(figsize=(size, size))
    ax.matshow(corr)
    plt.xticks(range(len(corr.columns)), corr.columns)
    plt.yticks(range(len(corr.columns)), corr.columns)


def visualise_predicted_results(y_test, y_pred):
    plt.figure(figsize=(15, 10))
    plt.scatter(y_test, y_pred)
    plt.xlabel("Actual prices")
    plt.ylabel("Predicted prices")
    plt.title("Actual vs Predicted prices")
    plt.show()


class LinearRegressionSerbian:

    def __init__(self, training_data, testing_data, x_train, y_train, x_test, y_test):
        self.training_data = training_data
        self.testing_data = testing_data
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.model = LinearRegression()

    def get_model(self):
        return self.model

    def train(self):
        start = time.time()
        self.model.fit(self.x_train, self.y_train)
        end = time.time()
        print()
        print("Linear regression:")
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


