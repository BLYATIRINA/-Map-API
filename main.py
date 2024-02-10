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

#Управление сейчас производится с помощью клавиш WASD.
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
        self.view = 'map'
        super().__init__()
        self.set_ui()
        self.get_map()


    def set_ui(self):
        self.label = QtWidgets.QLabel(self)
        self.label.resize(600, 450)
        self.resize(600, 450)
        self.scheme = QtWidgets.QPushButton(self)
        self.scheme.setText('Схема')
        self.scheme.move(300, 420)
        self.sputnic = QtWidgets.QPushButton(self)
        self.sputnic.setText('Спутник')
        self.sputnic.move(400, 420)
        self.hybride = QtWidgets.QPushButton(self)
        self.hybride.setText('Гибрид')
        self.hybride.move(500, 420)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.label)
        
        self.scheme.clicked.connect(lambda: self.change_view('map'))
        self.sputnic.clicked.connect(lambda: self.change_view('sat'))
        self.hybride.clicked.connect(lambda: self.change_view('sat,skl'))

    def change_view(self, view):
        self.view = view
        self.get_map()


    def get_map(self):
        params = {'ll': ','.join([self.long, self.lat]),
                  "l": self.view,
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
            if self.spn[0] > 90.0:
                self.spn = [90.0, 90.0]
            self.get_map()
        elif event.key() == Qt.Key_W:
            self.lat = str(float(self.lat) + self.spn[0])

            if float(self.lat) > 80.0:
                self.lat = str(-80.0)
            self.get_map()
        elif event.key() == Qt.Key_S:
            self.lat = str(float(self.lat) - self.spn[0])
            if float(self.lat) < -80.0:
                self.lat = str(80.0)

            self.get_map()

        elif event.key() == Qt.Key_A:


            self.long = str(float(self.long) - self.spn[0])
            if float(self.long) < -180.0:
                self.long = str(180.0)
            self.get_map()
        elif event.key() == Qt.Key_D:

            self.long = str(float(self.long) + self.spn[0])
            if float(self.long) > 180.0:
                self.long = str(-180.0)
            self.get_map()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    firstWnd = MainWindow()
    firstWnd.show()
    sys.exit(app.exec())