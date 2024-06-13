import sys
import subprocess

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFontMetrics, QPainter, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel


class VerticalLabel(QLabel):
    def __init__(self, *args):
        QLabel.__init__(self, *args)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(0, self.height())
        painter.rotate(-90)

        fm = QFontMetrics(painter.font())
        xoffset = int(fm.boundingRect(self.text()).width() / 2)
        yoffset = int(fm.boundingRect(self.text()).height() / 2)
        x = int(self.width() / 2) + yoffset
        y = int(self.height() / 2) - xoffset

        painter.drawText(y, x, self.text())
        painter.end()

    def minimumSizeHint(self):
        size = QLabel.minimumSizeHint(self)
        return QSize(size.height(), size.width())

    def sizeHint(self):
        size = QLabel.sizeHint(self)
        return QSize(size.height(), size.width())

    def wykrywacz_click(self, event):
        subprocess.run([sys.executable, 'classic_sweeper.py'])

    def skaner_click(self, event):
        subprocess.run([sys.executable, 'nasluchiwacz.py'])


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()

        top_buttons_layout = QVBoxLayout()
        self.exit_button = QPushButton("✖", self)
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setStyleSheet("QPushButton { background-color : red; color: white; font-size: 25px}");

        self.exit_button.setFixedWidth(90)
        self.exit_button.setFixedHeight(100)
        top_buttons_layout.addWidget(self.exit_button)
        top_buttons_layout.setAlignment(Qt.AlignBottom)
        main_layout.addLayout(top_buttons_layout)

        self.button1 = VerticalLabel('Wykrywacz podsłuchów', self)
        self.button1.mousePressEvent = self.button1.wykrywacz_click
        self.button1.setFont(QFont('Arial', 55))
        self.button1.setStyleSheet("QLabel { color : black; background-color: white;}");

        main_layout.addWidget(self.button1)

        self.button2 = VerticalLabel('Skan otoczenia', self)
        self.button2.mousePressEvent = self.button1.skaner_click
        self.button2.setFont(QFont('Arial', 55))
        self.button2.setStyleSheet("QLabel { color : black; background-color: white;}");

        main_layout.addWidget(self.button2)

        self.setLayout(main_layout)
        self.setWindowTitle('Main Window')
        self.showFullScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
