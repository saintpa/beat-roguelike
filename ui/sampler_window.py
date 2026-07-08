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
from systems.loop_manager import LoopManager


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

        self.loop_manager = LoopManager()
        self.waiting_for_loop_slot = False
        self.loop_play_timer = QTimer(self)
        self.loop_play_timer.timeout.connect(self.update_loop_playback)
        self.loop_play_timer.start(20)

        self.loop_playheads = {}
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

    def update_loop_playback(self):
        import time

        now = time.time()

        for slot_number, slot in self.loop_manager.slots.items():
            if not slot.is_playing or not slot.events or slot.length <= 0:
                continue

            if slot_number not in self.loop_playheads:
                self.loop_playheads[slot_number] = {
                    "start_time": now,
                    "next_event_index": 0,
                }

            playhead = self.loop_playheads[slot_number]
            elapsed = now - playhead["start_time"]

            if elapsed >= slot.length:
                playhead["start_time"] = now
                playhead["next_event_index"] = 0
                elapsed = 0

            while playhead["next_event_index"] < len(slot.events):
                event_time, action, pad_key, mode, bpm= slot.events[playhead["next_event_index"]]

                if event_time > elapsed:
                    break

                if action == "PLAY":
                    if mode == "natural":
                        self.pads[pad_key].toggle_repeat(0)

                    elif mode == "bpm" and bpm is not None:
                        self.pads[pad_key].toggle_repeat(bpm)

                    else:
                        self.pads[pad_key].trigger_pad()

                elif action == "STOP":
                    self.pads[pad_key].stop_pad()

                playhead["next_event_index"] += 1

    def keyPressEvent(self, event):
        if self.is_typing_bpm:
            self.handle_bpm_typing(event)
            return

        if self.waiting_for_loop_slot:
            slot_number = self.number_key_to_slot(event.key())

            if slot_number is not None:
                was_recording = self.loop_manager.slots[slot_number].is_recording

                self.loop_manager.toggle_recording(slot_number)

                if not was_recording:
                    active_pad_keys = self.get_active_repeat_pad_keys()
                    self.loop_manager.record_initial_active_pads(active_pad_keys)

                self.waiting_for_loop_slot = False
                return

        if event.key() == Qt.Key.Key_QuoteLeft:
            self.waiting_for_loop_slot = True
            print("Choose loop slot 0-9")
            return
        slot_number = self.number_key_to_slot(event.key())

        if slot_number is not None:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                self.kill_loop_slot(slot_number)
                return

            self.loop_manager.toggle_playback(slot_number)

            if self.loop_manager.slots[slot_number].is_playing:
                self.loop_playheads[slot_number] = {
                    "start_time": __import__("time").time(),
                    "next_event_index": 0,
                }
            else:
                self.loop_playheads.pop(slot_number, None)

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
                bpm = self.bpm_manager.get_bpm()
                self.pads[pressed_key].toggle_repeat(bpm)
                self.loop_manager.record_pad_press(pressed_key, "bpm", bpm)

            elif event.modifiers() & Qt.KeyboardModifier.AltModifier:
                self.pads[pressed_key].toggle_repeat(0)
                self.loop_manager.record_pad_press(pressed_key, "natural", None)

            elif event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                self.pads[pressed_key].stop_pad()
                self.loop_manager.record_pad_stop(pressed_key)

            else:
                self.pads[pressed_key].trigger_pad()
                self.loop_manager.record_pad_press(pressed_key, None, None)

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

    def number_key_to_slot(self, key):
        number_map = {
            Qt.Key.Key_1: 1,
            Qt.Key.Key_2: 2,
            Qt.Key.Key_3: 3,
            Qt.Key.Key_4: 4,
            Qt.Key.Key_5: 5,
            Qt.Key.Key_6: 6,
            Qt.Key.Key_7: 7,
            Qt.Key.Key_8: 8,
            Qt.Key.Key_9: 9,
            Qt.Key.Key_0: 0,
            # Shift + number symbols on keyboard
            Qt.Key.Key_Exclam: 1,  # !
            Qt.Key.Key_At: 2,  # @
            Qt.Key.Key_NumberSign: 3,  # #
            Qt.Key.Key_Dollar: 4,  # $
            Qt.Key.Key_Percent: 5,  # %
            Qt.Key.Key_AsciiCircum: 6,  # ^
            Qt.Key.Key_Ampersand: 7,  # &
            Qt.Key.Key_Asterisk: 8,  # *
            Qt.Key.Key_ParenLeft: 9,  # (
            Qt.Key.Key_ParenRight: 0,  # )
        }

        return number_map.get(key)

    def get_active_repeat_pad_keys(self):
        active_pads = []

        for key, pad in self.pads.items():
            if pad.repeat_enabled:
                active_pads.append((key, pad.loop_mode, pad.repeat_bpm))

        return active_pads

    def kill_loop_slot(self, slot_number):
        slot = self.loop_manager.slots[slot_number]

        pads_to_stop = set()

        for event_time, action, pad_key, mode, bpm in slot.events:
            if action == "PLAY":
                pads_to_stop.add(pad_key)

        self.loop_manager.stop_playback(slot_number)
        self.loop_playheads.pop(slot_number, None)

        for pad_key in pads_to_stop:
            if pad_key in self.pads:
                self.pads[pad_key].stop_pad()
