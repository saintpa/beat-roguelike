from PySide6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

from ui.pad_button import PadButton


class SamplerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Beat Roguelike")
        self.setFixedSize(800, 850)

        self.pads = {}

        main_layout = QVBoxLayout()

        melody_label = QLabel("MELODY")
        drum_label = QLabel("DRUMS")

        label_style = """
            QLabel {
                color: #ffcc66;
                font-size: 24px;
                font-weight: bold;
            }
        """

        melody_label.setStyleSheet(label_style)
        drum_label.setStyleSheet(label_style)

        melody_layout = QGridLayout()
        drum_layout = QGridLayout()

        melody_keys = [
            "Q",
            "W",
            "E",
            "A",
            "S",
            "D",
            "Z",
            "X",
            "C",
        ]

        drum_keys = [
            "I",
            "O",
            "P",
            "K",
            "L",
            ";",
            ",",
            ".",
            "/",
        ]

        for i, key in enumerate(melody_keys):
            pad = PadButton(key)
            self.pads[key] = pad
            melody_layout.addWidget(pad, i // 3, i % 3)

        for i, key in enumerate(drum_keys):
            pad = PadButton(key)
            self.pads[key] = pad
            drum_layout.addWidget(pad, i // 3, i % 3)

        main_layout.addWidget(melody_label)
        main_layout.addLayout(melody_layout)

        main_layout.addWidget(drum_label)
        main_layout.addLayout(drum_layout)

        self.setLayout(main_layout)

        self.setStyleSheet(
            """
            QWidget {
                background-color: #141010;
            }
        """
        )

    def keyPressEvent(self, event):
        key_map = {
            # Melody
            Qt.Key_Q: "Q",
            Qt.Key_W: "W",
            Qt.Key_E: "E",
            Qt.Key_A: "A",
            Qt.Key_S: "S",
            Qt.Key_D: "D",
            Qt.Key_Z: "Z",
            Qt.Key_X: "X",
            Qt.Key_C: "C",
            # Drums
            Qt.Key_I: "I",
            Qt.Key_O: "O",
            Qt.Key_P: "P",
            Qt.Key_K: "K",
            Qt.Key_L: "L",
            Qt.Key_Semicolon: ";",
            Qt.Key_Comma: ",",
            Qt.Key_Period: ".",
            Qt.Key_Slash: "/",
        }

        pressed_key = key_map.get(event.key())

        if pressed_key:
            self.pads[pressed_key].play_pad()
