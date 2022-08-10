from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score, accuracy_score, f1_score
import time


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
        self.model_newton = LogisticRegression(multi_class='multinomial', solver='newton-cg', max_iter=1000)
        self.model_saga = LogisticRegression(multi_class='multinomial', solver='saga', max_iter=1000)
        self.model_sag = LogisticRegression(multi_class='multinomial', solver='sag', max_iter=1000)

    def get_model(self, solver):
        switcher = {
            'newton-cg': self.model_newton,
            'saga': self.model_saga,
            'sag': self.model_sag
        }
        return switcher[solver]

    def train(self, solver):
        print()
        print("Multinomial logistic regression (solver: ", solver, "):")
        start = time.time()
        self.get_model(solver).fit(self.x_train, self.y_train)
        end = time.time()
        print("Training time: ", end - start, " seconds")
        self.evaluate_test_results(solver)

    def evaluate_test_results(self, solver):
        start = time.time()
        y_pred = self.get_model(solver).predict(self.x_test)
        end = time.time()
        print("Testing time: ", end - start, " seconds")
        evaluation = r2_score(self.y_test, y_pred)
        accuracy = accuracy_score(self.y_test, y_pred)
        f1 = f1_score(self.y_test, y_pred, average='weighted')
        print('Accuracy: ', "%.2f" % (accuracy * 100))
        print('F1: ', "%.2f" % (f1 * 100))
        print("R^2 (coefficient of determination) regression score function: ", evaluation)
        # visualise_predicted_results(self.y_test, y_pred)
