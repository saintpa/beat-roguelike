import sys
import pygame
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
from PySide6.QtCore import Qt

pygame.mixer.init()


class Sampler(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Beat Roguelike - Prototype 01")
        self.setFixedSize(700, 500)

        self.sound = pygame.mixer.Sound("sounds/4.mp3")

        layout = QGridLayout()

        keys = ["Q", "W", "E", "R", "A", "S", "D", "F"]

        for i, key in enumerate(keys):
            button = QPushButton(key)
            button.setFixedSize(140, 120)
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: #2b1d1d;
                    color: #ffcc66;
                    border: 4px solid #8b5a2b;
                    border-radius: 18px;
                    font-size: 32px;
                    font-weight: bold;
                }
                QPushButton:pressed {
                    background-color: #ff7a18;
                    color: black;
                }
            """
            )
            button.clicked.connect(self.play_sound)
            layout.addWidget(button, i // 4, i % 4)

        self.setLayout(layout)

    def play_sound(self):
        self.sound.play()

    def keyPressEvent(self, event):
        if event.key() in [
            Qt.Key_Q,
            Qt.Key_W,
            Qt.Key_E,
            Qt.Key_R,
            Qt.Key_A,
            Qt.Key_S,
            Qt.Key_D,
            Qt.Key_F,
        ]:
            self.play_sound()


app = QApplication(sys.argv)
window = Sampler()
window.show()
sys.exit(app.exec())
