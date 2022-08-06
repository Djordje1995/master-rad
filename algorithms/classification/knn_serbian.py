import math
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, r2_score
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import time


def score(knn_model, x_test, y_test):
    print("KNN Score: ")
    print(knn_model.score(x_test, y_test))


# def train_one(metric, params, x_train, y_train, x_test, y_test, test_data):
#     visualise(knn_model, x_train, y_train)
#     # visualise(knn_model, x_test, y_test)
#     score(knn_model, x_test, y_test)
#     y_pred = knn_model.predict(x_test)
#     print(set(y_test) - set(y_pred))
#     print_classification_report(y_test, y_pred)


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


class KNNSerbian:

    def __init__(self, training_data, testing_data, x_train, y_train, x_test, y_test):
        self.training_data = training_data
        self.testing_data = testing_data
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.k = round(math.sqrt(len(self.x_train)))
        self.model_euclidean = KNeighborsClassifier(n_neighbors=self.k, metric='euclidean', algorithm='auto', n_jobs=1)
        self.model_manhattan = KNeighborsClassifier(n_neighbors=self.k, metric='manhattan', algorithm='auto', n_jobs=1)
        self.model_chebyshev = KNeighborsClassifier(n_neighbors=self.k, metric='chebyshev', algorithm='auto', n_jobs=1)
        self.model_minkowski = KNeighborsClassifier(n_neighbors=self.k, metric='minkowski', algorithm='auto', n_jobs=1)
        self.model_cosine = KNeighborsClassifier(n_neighbors=self.k, metric='cosine', algorithm='auto', n_jobs=1)

    def get_model(self, metric):
        switcher = {
            "euclidean": self.model_euclidean,
            "manhattan": self.model_manhattan,
            "chebyshev": self.model_chebyshev,
            "minkowski": self.model_minkowski,
            "cosine": self.model_cosine
        }
        return switcher[metric]

    def train(self, metric):
        start = time.time()
        self.get_model(metric).fit(self.x_train, self.y_train)
        end = time.time()
        print()
        print("KNN (", metric, " metric):")
        print("Training time: ", end - start, " seconds")
        self.evaluate_test_results(metric)

    def evaluate_test_results(self, metric):
        start = time.time()
        pred = self.get_model(metric).predict(self.x_test)
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
