import sys
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from ui_file import Ui_MainWindow
import re


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.spn = 0.002

        self.camera = [0.0, 0.0]
        self.current_coord = [0.0, 0.0]
        
    def show_map(self):
        address = self.lineEdit.text()

        if len(address) != 0:
            sp = re.findall(r"\d*\.\d*", address)
            if len(sp) != 2:
                api_key = "8013b162-6b42-4997-9691-77b7074026e0"
                server_address = 'http://geocode-maps.yandex.ru/1.x/?'
                geocoder_request = f'{server_address}apikey={api_key}&geocode={address}&format=json'
                print(geocoder_request)
                response = requests.get(geocoder_request)
                if response:
                    json_response = response.json()
                    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                    toponym_coodrinates = toponym["Point"]["pos"]
                    sp = toponym_coodrinates.split(' ')
                    sp.reverse()
                    self.current_coord = sp.copy()
                    self.camera = list(map(float, sp))
                else:
                    print('Неверный запрос')
            server_address = 'https://static-maps.yandex.ru/v1?'
            print(self.camera)
            ll_spn = f'll={self.camera[1]},{self.camera[0]}&spn={self.spn},{self.spn}'
            api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
            map_request = f"{server_address}{ll_spn}&apikey={api_key}"
            response = requests.get(map_request)
            if not response:
                print("Ошибка выполнения запроса:")
                print(map_request)
                print("Http статус:", response.status_code, "(", response.reason, ")")
            map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)
            self.pixmap = QPixmap(map_file)
            self.label.setPixmap(self.pixmap)
    
    def clear(self):
        self.lineEdit.clear()
        self.label.clear()
        self.spn = 0.002
        self.camera = [0.0, 0.0]
        self.current_coord = [0.0, 0.0]
    
    def find(self):
        self.spn = 0.002
        self.show_map()
        self.setFocus()
    
    def keyPressEvent(self, event):
        if event.key() in [Qt.Key.Key_PageUp, Qt.Key.Key_PageDown, Qt.Key.Key_Up,  Qt.Key.Key_Down, Qt.Key.Key_Left,  Qt.Key.Key_Right]:
            if event.key() == Qt.Key.Key_PageUp:
                self.spn /= 2
            elif event.key() == Qt.Key.Key_PageDown:
                self.spn = min(64, self.spn * 2)
            elif event.key() == Qt.Key.Key_Up:
                print(1)
                self.camera[0] += 100 * self.spn
            elif event.key() == Qt.Key.Key_Down:
                print(1)
                self.camera[0] -= 100 * self.spn
            elif event.key() == Qt.Key.Key_Left:
                print(1)
                self.camera[1] -= 100 * self.spn
            elif event.key() == Qt.Key.Key_Right:
                print(1)
                self.camera[1] += 100 * self.spn
            self.show_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())