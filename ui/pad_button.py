import os

from PySide6.QtWidgets import QPushButton, QFileDialog
from PySide6.QtCore import Qt

from audio.audio_engine import load_sound, play_sound


class PadButton(QPushButton):
    def __init__(self, key_name):
        super().__init__()

        self.key_name = key_name

        self.sound = None
        self.sound_path = None

        self.setFixedSize(160, 130)

        self.update_text()

        self.setStyleSheet(
            """

            QPushButton {
                background-color: #2b1d1d;
                color: #ffcc66;

                border: 4px solid #8b5a2b;
                border-radius: 18px;

                font-size: 22px;
                font-weight: bold;
            }

            QPushButton:pressed {

                background-color: #ff7a18;
                color: black;
            }

        """
        )

        self.clicked.connect(self.play_pad)

    def update_text(self):
        if self.sound_path:
            filename = os.path.basename(self.sound_path)

            self.setText(f"{self.key_name}\n{filename}")

        else:
            self.setText(f"{self.key_name}\nEMPTY")

    def load_pad_sound(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Choose Sound", "", "Audio Files (*.wav *.mp3 *.ogg)"
        )

        if file_path:
            self.sound_path = file_path

            self.sound = load_sound(file_path)

            self.update_text()

    def play_pad(self):
        play_sound(self.sound)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.load_pad_sound()

        else:
            super().mousePressEvent(event)
