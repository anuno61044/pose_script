import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import cv2

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Camara y Foto')
        self.setGeometry(300, 300, 800, 600)

        layout = QVBoxLayout()

        self.label_camara = QLabel(self)
        self.label_camara.setAlignment(Qt.AlignCenter)

        self.label_foto = QLabel(self)
        self.label_foto.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label_camara)
        layout.addWidget(self.label_foto)

        self.setLayout(layout)

        self.show_video()

    def show_video(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = QPixmap.fromImage(qt_image)
            self.label_camara.setPixmap(p)

            # Cargar y mostrar la foto
            self.label_foto.setPixmap(QPixmap('ruta/a/tu/foto.jpg'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())