import csv_handler
import pandas as pd
import column_value_calculator_serbian
import linear_regression_serbian
import median_calculator_serbian

MARKA = 'Marka'
MODEL = 'Model'
GODISTE = 'Godište'
KILOMETRAZA = 'Kilometraža'
KAROSERIJA = 'Karoserija'
GORIVO = 'Gorivo'
KUBIKAZA = 'Kubikaža'
SNAGA_MOTORA = 'Snaga motora'
EMISIONA_KLASA_MOTORA = 'Emisiona klasa motora'
POGON = 'Pogon'
MENJAC = 'Menjač'
CENA = 'Cena'

PREDIKCIONA_CENA = 'Predikciona cena'
APSOLUTNA_RAZLIKA = 'Apsolutna razlika'
PROCENAT = 'Procenat'


def fill_data(row, x, y):
    """ fills the corresponding x and y matrix for linear regression"""
    temp = []
    for item in row:
        if item in csv_handler.new_serbian_headers:
            if item == CENA:
                y.append(int(row[item]))
            else:
                temp.append(column_value_calculator_serbian.get_calculated_values(item, row[item]))
    x.append(temp)


def call_all_algorithms():
    median_calculator_serbian.populate_lists()
    learning_data = csv_handler.get_learning_data_serbian()
    testing_data = csv_handler.get_testing_data_serbian()
    x = []
    y = []
    for row in learning_data:
        fill_data(row, x, y)
    xd = pd.DataFrame(x)
    yd = pd.DataFrame(y)
    x_test = []
    y_test = []
    for row in testing_data:
        fill_data(row, x_test, y_test)

    # call linear regression algorithm
    linear_regression_serbian.train(x, y, x_test, y_test)


call_all_algorithms()
