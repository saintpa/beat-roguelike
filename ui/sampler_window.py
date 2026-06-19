from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel

from PySide6.QtCore import Qt

from ui.pad_button import PadButton


class SamplerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Beat Roguelike")
        self.resize(1200, 700)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.pads = {}

        main_layout = QHBoxLayout()

        melody_section = self.create_pad_section(
            title="MELODY",
            keys=[
                "Q",
                "W",
                "E",
                "A",
                "S",
                "D",
                "Z",
                "X",
                "C",
            ],
        )

        drum_section = self.create_pad_section(
            title="DRUMS",
            keys=[
                "I",
                "O",
                "P",
                "K",
                "L",
                ";",
                ",",
                ".",
                "/",
            ],
        )

        main_layout.addLayout(melody_section)
        main_layout.addLayout(drum_section)

        self.setLayout(main_layout)

        self.setStyleSheet(
            """
            QWidget {
                background-color: #141010;
            }
        """
        )

    def create_pad_section(self, title, keys):
        section_layout = QVBoxLayout()

        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label.setStyleSheet(
            """
            QLabel {
            color: #ffcc66;
            font-size: 28px;
            font-weight: bold;
                }"""
        )
        grid = QGridLayout()

        for i, key in enumerate(keys):
            pad = PadButton(key, len(self.pads))
            self.pads[key] = pad
            grid.addWidget(pad, i // 3, i % 3)

        section_layout.addWidget(label)
        section_layout.addLayout(grid)

        return section_layout

    def keyPressEvent(self, event):
        key_map = {
            Qt.Key.Key_Q: "Q",
            Qt.Key.Key_W: "W",
            Qt.Key.Key_E: "E",
            Qt.Key.Key_A: "A",
            Qt.Key.Key_S: "S",
            Qt.Key.Key_D: "D",
            Qt.Key.Key_Z: "Z",
            Qt.Key.Key_X: "X",
            Qt.Key.Key_C: "C",
            Qt.Key.Key_I: "I",
            Qt.Key.Key_O: "O",
            Qt.Key.Key_P: "P",
            Qt.Key.Key_K: "K",
            Qt.Key.Key_L: "L",
            Qt.Key.Key_Semicolon: ";",
            Qt.Key.Key_Comma: ",",
            Qt.Key.Key_Period: ".",
            Qt.Key.Key_Slash: "/",
        }

        pressed_key = key_map.get(event.key())

        if pressed_key:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                self.pads[pressed_key].stop_pad()
            else:
                self.pads[pressed_key].trigger_pad()
