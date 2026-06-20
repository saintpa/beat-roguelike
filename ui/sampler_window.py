from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
)

from PySide6.QtCore import Qt, QTimer

from ui.pad_button import PadButton
from systems.kit_manager import load_kit_file
from systems.bpm_manager import BPMManager


class SamplerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Beat Roguelike")
        self.resize(1200, 700)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.pads = {}

        self.bpm_manager = BPMManager()
        self.is_typing_bpm = False
        self.bpm_input = ""

        self.metronome_on = False
        self.metronome_timer = QTimer(self)
        self.metronome_timer.timeout.connect(self.metronome_tick)

        root_layout = QVBoxLayout()
        top_bar = QHBoxLayout()
        main_layout = QHBoxLayout()

        load_kit_button = QPushButton("Load Kit JSON")
        load_kit_button.clicked.connect(self.open_kit_file)

        self.bpm_label = QLabel(f"BPM: {self.bpm_manager.get_bpm()}")
        self.bpm_label.setStyleSheet(
            """
            QLabel {
                color: #4de1ff;
                font-size: 22px;
                font-weight: bold;
            }
        """
        )

        self.metronome_button = QPushButton("Metronome OFF")
        self.metronome_button.clicked.connect(self.toggle_metronome)

        top_bar.addWidget(load_kit_button)
        top_bar.addWidget(self.bpm_label)
        top_bar.addWidget(self.metronome_button)
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
            }
        """
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
        if self.is_typing_bpm:
            self.handle_bpm_typing(event)
            return

        if event.key() == Qt.Key.Key_BracketRight:
            self.start_bpm_input()
            return

        if event.key() == Qt.Key.Key_Minus:
            self.bpm_manager.decrease()
            self.update_bpm_label()
            return

        if event.key() == Qt.Key.Key_Equal:
            self.bpm_manager.increase()
            self.update_bpm_label()
            return

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
            if (
                event.modifiers() & Qt.KeyboardModifier.AltModifier
                and event.modifiers() & Qt.KeyboardModifier.ShiftModifier
            ):
                self.pads[pressed_key].toggle_repeat(self.bpm_manager.get_bpm())

            elif event.modifiers() & Qt.KeyboardModifier.AltModifier:
                self.pads[pressed_key].toggle_repeat(0)
            elif event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                self.pads[pressed_key].stop_pad()

            else:
                self.pads[pressed_key].trigger_pad()

    def handle_bpm_typing(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.confirm_bpm_input()
            return

        if event.key() == Qt.Key.Key_Escape:
            self.cancel_bpm_input()
            return

        if event.key() == Qt.Key.Key_Backspace:
            self.bpm_input = self.bpm_input[:-1]
            self.update_bpm_label()
            return

        text = event.text()

        if text.isdigit():
            self.bpm_input += text
            self.update_bpm_label()

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

    def update_bpm_label(self):
        if self.is_typing_bpm:
            self.bpm_label.setText(f"BPM: {self.bpm_input}_")
        else:
            self.bpm_label.setText(f"BPM: {self.bpm_manager.get_bpm()}")

        if self.metronome_on:
            self.metronome_timer.start(self.bpm_to_interval_ms())

    def start_bpm_input(self):
        self.is_typing_bpm = True
        self.bpm_input = ""
        self.update_bpm_label()

    def confirm_bpm_input(self):
        if self.bpm_input:
            self.bpm_manager.set_bpm(int(self.bpm_input))

        self.is_typing_bpm = False
        self.bpm_input = ""
        self.update_bpm_label()

    def cancel_bpm_input(self):
        self.is_typing_bpm = False
        self.bpm_input = ""
        self.update_bpm_label()

    def bpm_to_interval_ms(self):
        bpm = self.bpm_manager.get_bpm()
        return int(60000 / bpm)

    def toggle_metronome(self):
        self.metronome_on = not self.metronome_on

        if self.metronome_on:
            self.metronome_button.setText("Metronome ON")
            self.metronome_timer.start(self.bpm_to_interval_ms())
        else:
            self.metronome_button.setText("Metronome OFF")
            self.metronome_timer.stop()

    def metronome_tick(self):
        print("tick")
