import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton, QHBoxLayout,
)
from PyQt5.QtGui import QFont, QFontMetrics, QPainter
from PyQt5.QtCore import Qt, QTimer, QSize


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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Timer")
        self.setGeometry(100, 100, 960, 540)

        central_widget = QWidget()
        main_layout = QHBoxLayout()

        top_buttons_layout = QVBoxLayout()
        self.exit_button = QPushButton("✖", self)
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setStyleSheet("QPushButton { background-color : red; color: white; font-size: 25px}");

        self.exit_button.setFixedWidth(50)
        self.exit_button.setFixedHeight(50)
        top_buttons_layout.addWidget(self.exit_button)
        top_buttons_layout.setAlignment(Qt.AlignTop)
        main_layout.addLayout(top_buttons_layout)

        self.timer_label = VerticalLabel("Czas: 0:00 s")
        self.timer_label.setFont(QFont('Arial', 100))
        self.timer_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.timer_label)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.time = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # update every second

        self.showFullScreen()

    def update_time(self):
        self.time += 1
        minutes, seconds = divmod(self.time, 60)
        self.timer_label.setText(f"Czas: {minutes}:{seconds:02d} s")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
