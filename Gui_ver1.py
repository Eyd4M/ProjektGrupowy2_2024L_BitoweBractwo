import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from PyQt5.QtGui import QColor, QPainter, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QSize


class LEDBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.num_leds = 15
        self.led_height = 80
        self.led_width = 40
        self.led_spacing = 5
        self.min_db = -12.0
        self.max_db = 3.0
        self.signal_strength = 0
        self.setMinimumSize(
            (self.num_leds * (self.led_width + self.led_spacing) - self.led_spacing),
            self.led_height
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        step_size = (self.max_db - self.min_db) / (self.num_leds - 1)
        bar_width = self.num_leds * (self.led_width + self.led_spacing) - self.led_spacing
        bar_height = self.led_height
        x_offset = (self.width() - bar_width) // 2
        y_offset = (self.height() - bar_height) // 2

        for i in range(self.num_leds):
            db_value = self.min_db + i * step_size
            if self.signal_strength > db_value:
                color = QColor(255, 0, 0)
            else:
                color = QColor(100, 100, 100)
            painter.setBrush(color)
            painter.drawRect(
                x_offset + (self.num_leds - 1 - i) * (self.led_width + self.led_spacing),
                y_offset,
                self.led_width,
                self.led_height,
            )


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
        self.setWindowTitle("Wykrywacz podsłuchów")
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

        placeholder_layout = QVBoxLayout()

        self.lbl1 = VerticalLabel('Wykrywacz podsłuchów')
        self.lbl1.setFont(QFont('Arial', 55))
        self.lbl1.setStyleSheet("QLabel { color : black;}");
        placeholder_layout.addWidget(self.lbl1)
        placeholder_layout.addStretch()

        placeholder_layout_wrapper = QVBoxLayout()
        placeholder_layout_wrapper.addStretch()
        placeholder_layout_wrapper.addLayout(placeholder_layout)
        placeholder_layout_wrapper.addStretch()

        main_layout.addLayout(placeholder_layout_wrapper)

        ledbar_layout = QVBoxLayout()
        ledbar_layout.addStretch()
        self.led_bar = LEDBar(self)
        ledbar_layout.addWidget(self.led_bar)
        ledbar_layout.addStretch()
        main_layout.addLayout(ledbar_layout)

        value_layout = QVBoxLayout()

        self.lbl3 = VerticalLabel('loading...')
        self.lbl3.setFont(QFont('Arial', 35))
        self.lbl3.setStyleSheet("QLabel { color : black; margin: 0px 20px 0px 20px;}");
        value_layout.addWidget(self.lbl3)

        v_widget = QWidget()
        v_widget.setLayout(value_layout)
        v_widget.setFixedWidth(40)

        main_layout.addWidget(v_widget)

        low_layout = QVBoxLayout()
        low_layout.setAlignment(Qt.AlignCenter)

        self.right_button = QPushButton("↑", self)
        self.right_button.clicked.connect(self.increase_state)
        self.right_button.setStyleSheet("QPushButton { font-size: 50px; padding: 15px; }")
        low_layout.addWidget(self.right_button)

        self.lbl2 = VerticalLabel(' 38MHz - 43MHz ')
        self.lbl2.setFont(QFont('Arial', 45))
        self.lbl2.setStyleSheet("QLabel { color : black; margin: 0px 20px 0px 20px; min-with: 300px}");
        low_layout.addWidget(self.lbl2)
        low_layout.addStretch()

        self.left_button = QPushButton("↓", self)
        self.left_button.clicked.connect(self.decrease_state)
        self.left_button.setStyleSheet("QPushButton { font-size: 50px; padding: 10px; }")
        low_layout.addWidget(self.left_button)

        low_layout_wrapper = QVBoxLayout()
        low_layout_wrapper.addStretch()
        low_layout_wrapper.addLayout(low_layout)
        low_layout_wrapper.addStretch()

        main_layout.addLayout(low_layout_wrapper)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.current_state = 0
        self.showFullScreen()

    def update_led(self, value, min_db, max_db):
        self.led_bar.signal_strength = value
        self.lbl3.setText(f"P: {value:.2f} dBm")
        self.lbl3.update()
        self.update()

    def decrease_state(self):
        self.current_state = (self.current_state - 1) % 5
        if(self.current_state == 0): self.lbl2.setText(f"38MHz - 43MHz")
        elif (self.current_state == 1): self.lbl2.setText(f"100MHz - 110MHz")
        elif (self.current_state == 2): self.lbl2.setText(f"200MHz - 220MHz")
        elif (self.current_state == 3): self.lbl2.setText(f"430MHz - 440MHz")
        elif (self.current_state == 4): self.lbl2.setText(f"865MHz - 870MHz")
        self.lbl2.update()

    def increase_state(self):
        self.current_state = (self.current_state + 1) % 5
        if (self.current_state == 0):self.lbl2.setText(f"38MHz - 43MHz")
        elif (self.current_state == 1):self.lbl2.setText(f"100MHz - 110MHz")
        elif (self.current_state == 2):self.lbl2.setText(f"200MHz - 220MHz")
        elif (self.current_state == 3):self.lbl2.setText(f"430MHz - 440MHz")
        elif (self.current_state == 4):self.lbl2.setText(f"865MHz - 870MHz")
        self.lbl2.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
