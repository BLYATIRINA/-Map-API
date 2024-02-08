from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import sys
import requests
from mapapi import MainWindow_Ui
from PIL import Image
from io import BytesIO

MAP_API_SERVER = "http://static-maps.yandex.ru/1.x/"
MAP_FILENAME = 'map.png'
class MainWindow(QtWidgets.QMainWindow, MainWindow_Ui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_map)

    def get_map(self):
        long = self.lineEdit.text()
        lat = self.lineEdit_2.text()
        params = {'ll': ','.join([long, lat]),
                  "l": "map",}
        response = requests.get(MAP_API_SERVER, params=params)
        self.scndWnd = Map_Window(response)
        self.scndWnd.show()



class Map_Window(QtWidgets.QMainWindow):

    def __init__(self, response):
        super().__init__()
        self.set_ui(response)

    def set_ui(self, response):
        with open(MAP_FILENAME, 'wb') as file:
            file.write(response.content)
        self.label = QtWidgets.QLabel(self)
        pixmap = QPixmap(MAP_FILENAME)
        self.label.resize(600, 450)
        self.resize(pixmap.width(), pixmap.height())
        self.label.setPixmap(pixmap)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.label)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    firstWnd = MainWindow()
    firstWnd.show()
    sys.exit(app.exec())