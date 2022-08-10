import sys
from PyQt5.QtWidgets import QApplication, QDialog
from utils import util, constant
import price_prediction_gui
from loading_indicator import LoadingIndicator
from all_algorithms import Algorithms


algorithms = [
                'Linear regression',
                'Polynomial regression',
                'Lasso regression',
                'Ridge regression',
                'Multinomial logistic regression (solver: newton-cg)',
                'Multinomial logistic regression (solver: saga)',
                'Multinomial logistic regression (solver: sag)',
                'Naive bayes',
                'Support vector machine (kernel: polynomial)',
                'Support vector machine (kernel: rbf)',
                'K Nearest neighbours euclidean',
                'K Nearest neighbours manhattan',
                'K Nearest neighbours chebyshev',
                'K Nearest neighbours minkowski',
                'K Nearest neighbours cosine',
                'Random forests classifier'
              ]


class MyApp(QDialog, price_prediction_gui.Ui_Dialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.init_combo_box()
        self.brand_select.currentIndexChanged.connect(self.update_model_select_box)
        self.predict_button.pressed.connect(self.fire_prediction)

        # self.loading_indicator = LoadingIndicator()
        self.all_algorithms = Algorithms()

        # self.loading_indicator.startAnimation()
        self.all_algorithms.train_all_algorithms()
        # self.loading_indicator.stopAnimation()

    def init_combo_box(self):
        brands_with_modules = util.get_brands_with_modules()
        for item in list(brands_with_modules.keys()):
            self.brand_select.addItem(item, brands_with_modules[item])
        self.model_select.addItems(self.brand_select.itemData(0))
        self.algorithm_selection.addItems(algorithms)

    def update_model_select_box(self, index):
        self.model_select.clear()
        models = self.brand_select.itemData(index)
        if models:
            self.model_select.addItems(models)

    def fire_prediction(self):
        form_data = {
            constant.MODEL: str(self.brand_select.currentText()) + " : " + str(self.model_select.currentText()),
            constant.GODISTE: int(self.year_edit.text()),
            constant.KILOMETRAZA: int(self.mileage_edit.text()),
            constant.KUBIKAZA: int(self.engine_size_edit.text()),
            constant.SNAGA_MOTORA: int(self.engine_power_edit.text())
            }
        algorithm = str(self.algorithm_selection.currentText())
        predicted_value = self.all_algorithms.predict(form_data, algorithm)
        self.prediction_price_edit.setText(predicted_value)


app = QApplication(sys.argv)
my_app = MyApp()
my_app.show()
app.exec_()
