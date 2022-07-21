from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import constant
import k_nearest_neighbors


def prepare_price_data(data):
    prices = data[constant.PRICE]
    lista = []
    for row in prices.tolist():
        if float(row) < 5000:
            item = 0
        elif 5000 <= float(row) < 10000:
            item = 1
        elif 10000 <= float(row) < 15000:
            item = 2
        elif 15000 <= float(row) < 20000:
            item = 3
        elif 20000 <= float(row) < 25000:
            item = 4
        elif 25000 <= float(row) < 30000:
            item = 5
        else:
            item = 6
        lista.append(item)
    data[constant.PRICE] = pd.Series(lista)


def visualize_confusion_matrix(cm):
    plt.figure(figsize=(7, 7))
    sns.heatmap(cm, annot=True, count=True)
    plt.xlabel("Predicted")
    plt.ylabel("Truth")
    plt.show()


def visualize():
    learning_data = pd.read_csv(constant.DATA_FOLDER + constant.LEARNING_DATA + constant.CSV)
    # k_nearest_neighbors.train()
    prepare_price_data(learning_data)
    plt.close()
    # sns.set_style("whitegrid")
    # sns.pairplot(learning_data, hue=constant.PRICE, height=5)
    sns.set_style("whitegrid")
    sns.FacetGrid(learning_data, hue=constant.PRICE, height=5)\
        .map(plt.scatter, constant.FUEL_TYPE, constant.YEAR).add_legend()
    plt.show()
