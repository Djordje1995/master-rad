from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget, QLabel


class LoadingIndicator(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(77, 77)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)

        self.label_animation = QLabel(self)
        self.movie = QMovie('loading_indicator_small.gif')
        self.label_animation.setMovie(self.movie)
        self.label_animation.setFixedSize(77, 77)

        self.show()

    def startAnimation(self):
        self.movie.start()

    def stopAnimation(self):
        self.movie.stop()
        self.close()
