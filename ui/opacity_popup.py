from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt

class OpacityPopup(QWidget):
    def __init__(self, parent_window):
        super().__init__(parent_window, Qt.Popup)
        self.parent_window = parent_window
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0.9); border-radius: 8px; border: 1px solid #e0e0e0;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(10)
        self.slider.setMaximum(100)
        self.slider.setValue(int(self.parent_window.windowOpacity() * 100))
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #f0f0f0;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #1565c0;
                border: 1px solid #1565c0;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
        """)
        self.slider.valueChanged.connect(self.slider_value_changed)
        layout.addWidget(self.slider)
        self.setLayout(layout)
        self.setFixedSize(200, 40)
    def slider_value_changed(self, value):
        self.parent_window.set_window_opacity(value / 100.0)
    def show_at(self, pos):
        self.move(pos)
        self.show() 