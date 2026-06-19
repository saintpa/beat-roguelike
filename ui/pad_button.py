import os

from PySide6.QtWidgets import QPushButton, QFileDialog
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor

from audio.audio_engine import (
    load_sound,
    get_channel,
    play_sound_on_channel,
    stop_channel,
)


class PadButton(QPushButton):
    def __init__(self, key_name, channel_id):
        super().__init__()

        self.key_name = key_name
        self.sound = None
        self.sound_path = None

        # Each pad owns one permanent audio channel.
        self.channel = get_channel(channel_id)

        self.progress = 0
        self.progress_step = 0
        self.timer_step_ms = 30

        self.play_timer = QTimer(self)
        self.play_timer.timeout.connect(self.update_progress)

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
            self.setText(f"{self.key_name}\n{self.short_filename(filename)}")
        else:
            self.setText(f"{self.key_name}\nEMPTY")

    def short_filename(self, filename, max_length=14):
        if len(filename) <= max_length:
            return filename

        return filename[: max_length - 3] + "..."

    def load_pad_sound(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Sound",
            "",
            "Audio Files (*.wav *.mp3 *.ogg)",
        )

        if file_path:
            self.sound_path = file_path
            self.sound = load_sound(file_path)
            self.update_text()
            print(f"Loaded sound for {self.key_name}: {file_path}")

    def trigger_pad(self):
        self.stop_pad()
        self.flash()

        if not self.sound:
            print(f"No sound loaded for pad {self.key_name}")
            return

        play_sound_on_channel(self.sound, self.channel)

        self.setText("")

        duration_ms = int(self.sound.get_length() * 1000)

        self.progress = 0
        self.progress_step = 1 / max(duration_ms / self.timer_step_ms, 1)

        self.play_timer.start(self.timer_step_ms)

    def stop_pad(self):
        stop_channel(self.channel)

        self.progress = 0
        self.progress_step = 0
        self.play_timer.stop()

        self.update_text()
        self.setStyleSheet(self.normal_style)
        self.update()

    def update_progress(self):
        self.progress += self.progress_step

        if self.progress >= 1:
            self.progress = 0
            self.progress_step = 0
            self.play_timer.stop()
            self.update_text()
            self.update()
            return

        self.update()

    def flash(self):
        self.setStyleSheet(self.active_style)
        QTimer.singleShot(150, self.reset_style)

    def reset_style(self):
        self.setStyleSheet(self.normal_style)

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.progress <= 0 or self.progress >= 1:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        size = min(self.width(), self.height()) - 28

        rect = QRectF(
            (self.width() - size) / 2,
            (self.height() - size) / 2,
            size,
            size,
        )

        painter.setPen(Qt.PenStyle.NoPen)

        fill_color = QColor("#4de1ff")
        fill_color.setAlpha(180)
        painter.setBrush(fill_color)

        start_angle = 90 * 16
        span_angle = int(-360 * self.progress * 16)

        painter.drawPie(rect, start_angle, span_angle)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.load_pad_sound()
        else:
            super().mousePressEvent(event)
