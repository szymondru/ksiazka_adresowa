import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from gui_main import ProgramGlowny



if __name__ == "__main__":
    app = QApplication(sys.argv)
    if os.path.exists("logo.svg"):
        app_icon = QIcon("logo.svg")
        app.setWindowIcon(app_icon)
    window = ProgramGlowny()
    window.show()
    sys.exit(app.exec())
