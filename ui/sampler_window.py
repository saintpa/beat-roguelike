from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
)

from PySide6.QtCore import Qt

from ui.pad_button import PadButton

from systems.kit_manager import load_kit_file


class SamplerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Beat Roguelike")
        self.resize(1200, 700)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.pads = {}

        root_layout = QVBoxLayout()
        top_bar = QHBoxLayout()
        main_layout = QHBoxLayout()

        load_kit_button = QPushButton("Load Kit JSON")
        load_kit_button.clicked.connect(self.open_kit_file)

        top_bar.addWidget(load_kit_button)
        top_bar.addStretch()

        root_layout.addLayout(top_bar)
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

        root_layout.addLayout(main_layout)
        self.setLayout(root_layout)

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

    def open_kit_file(self):
        kit_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Kit JSON",
            "",
            "JSON Files (*.json)",
        )

        if kit_path:
            self.load_kit(kit_path)

    def load_kit(self, kit_path):
        kit_data = load_kit_file(kit_path)

        for key, sound_path in kit_data.items():
            if key in self.pads:
                self.pads[key].load_sound_from_path(sound_path)
