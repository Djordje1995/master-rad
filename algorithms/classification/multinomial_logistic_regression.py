from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score


def visualise_predicted_results(y_test, y_pred):
    plt.figure(figsize=(15, 10))
    plt.scatter(y_test, y_pred)
    plt.xlabel("Actual prices")
    plt.ylabel("Predicted prices")
    plt.title("Actual vs Predicted prices")
    plt.show()


class MultinomialLogisticRegressionSerbian:

    def __init__(self, training_data, testing_data, x_train, y_train, x_test, y_test):
        self.training_data = training_data
        self.testing_data = testing_data
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=100000)

    def get_model(self):
        return self.model

    def train(self):
        self.model.fit(self.x_train, self.y_train)
        self.evaluate_test_results()

    def evaluate_test_results(self):
        y_pred = self.model.predict(self.x_test)
        evaluation = r2_score(self.y_test, y_pred)
        print("Multinomial logistic regression:")
        print("R^2 (coefficient of determination) regression score function:")
        print(evaluation)
        # visualise_predicted_results(self.y_test, y_pred)
