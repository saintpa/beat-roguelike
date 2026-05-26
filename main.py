import sys

from PySide6.QtWidgets import QApplication

from ui.sampler_window import SamplerWindow


app = QApplication(sys.argv)

window = SamplerWindow()

window.show()

sys.exit(app.exec())

