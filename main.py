from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import sys
import requests
from mapapi import MainWindow_Ui
from PyQt5.QtCore import Qt
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
        global params
        long = self.lineEdit.text()
        lat = self.lineEdit_2.text()
        self.scndWnd = Map_Window(long, lat)
        self.scndWnd.show()


class Map_Window(QtWidgets.QMainWindow):

    def __init__(self, long, lat):
        self.spn = [3.0, 3.0]
        self.long = long
        self.lat = lat
        super().__init__()
        self.set_ui()
        self.get_map()


    def set_ui(self):
        self.label = QtWidgets.QLabel(self)
        self.label.resize(600, 450)
        self.resize(600, 450)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.label)


    def get_map(self):
        print(','.join(list(map(str, self.spn))))
        params = {'ll': ','.join([self.long, self.lat]),
                  "l": "map",
                  'spn': ','.join(list(map(str, self.spn)))}
        response = requests.get(MAP_API_SERVER, params=params)
        with open(MAP_FILENAME, 'wb') as file:
            file.write(response.content)
        pixmap = QPixmap(MAP_FILENAME)
        self.label.setPixmap(pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.spn = [i - i / 2 for i in self.spn]
            self.get_map()
        elif event.key() == Qt.Key_PageDown:
            self.spn = [i + i / 2 for i in self.spn]
            print(','.join(list(map(str, self.spn))))
            if self.spn[0] > 90.0:
                self.spn = [90.0, 90.0]
            self.get_map()
        elif event.key() == Qt.Key_Up:
            print(self.long)
            self.lat = str(float(self.lat) + self.spn[0])
            self.get_map()
        elif event.key() == Qt.Key_Down:
            self.lat = str(float(self.lat) - self.spn[0])
            self.get_map()
        elif event.key() == Qt.Key_Left:
            print(self.long)
            self.long = str(float(self.long) - self.spn[0])
            self.get_map()
        elif event.key() == Qt.Key_Right:
            self.long = str(float(self.long) + self.spn[0])
            self.get_map()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    firstWnd = MainWindow()
    firstWnd.show()
    sys.exit(app.exec())