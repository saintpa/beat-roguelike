import os

from PySide6.QtWidgets import QPushButton, QFileDialog
from PySide6.QtCore import Qt, QTimer

from audio.audio_engine import load_sound, play_sound


class PadButton(QPushButton):
    def __init__(self, key_name):
        super().__init__()

        self.key_name = key_name
        self.sound = None
        self.sound_path = None

        self.setMinimumSize(140, 120)

        self.normal_style = """
            QPushButton {
                background-color: #2b1d1d;
                color: #ffcc66;
                border: 4px solid #8b5a2b;
                border-radius: 18px;
                font-size: 20px;
                font-weight: bold;
            }
        """

        self.active_style = """
            QPushButton {
                background-color: #ff7a18;
                color: black;
                border: 4px solid #ffcc66;
                border-radius: 18px;
                font-size: 20px;
                font-weight: bold;
            }
        """

        self.setStyleSheet(self.normal_style)
        self.update_text()

        self.clicked.connect(self.trigger_pad)

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
            print(f"Loaded sound for {self.key_name}: {file_path}")

    def trigger_pad(self):
        self.flash()

        if self.sound:
            play_sound(self.sound)
        else:
            print(f"No sound loaded for pad {self.key_name}")

    def flash(self):
        self.setStyleSheet(self.active_style)

        QTimer.singleShot(150, self.reset_style)

    def reset_style(self):
        self.setStyleSheet(self.normal_style)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.load_pad_sound()
        else:
            super().mousePressEvent(event)
