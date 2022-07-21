import sys
from PyQt5.QtWidgets import QApplication, QDialog
import util
import price_prediction_gui
import loading_indicator


class MyApp(QDialog, price_prediction_gui.Ui_Dialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.init_combo_box()
        self.brand_select.currentIndexChanged.connect(self.update_model_select_box)

        self.loading_indicator = loading_indicator.LoadingIndicator()

    def init_combo_box(self):
        brands_with_modules = util.get_brands_with_modules()
        for item in list(brands_with_modules.keys()):
            self.brand_select.addItem(item, brands_with_modules[item])
        self.model_select.addItems(self.brand_select.itemData(0))

    def update_model_select_box(self, index):
        self.model_select.clear()
        models = self.brand_select.itemData(index)
        if models:
            self.model_select.addItems(models)


app = QApplication(sys.argv)
my_app = MyApp()
my_app.show()
app.exec_()
