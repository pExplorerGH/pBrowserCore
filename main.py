# main.py
import sys
from PyQt5.QtWidgets import QApplication
from browser_window import BrowserWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Simple Browser")

    window = BrowserWindow()
    window.show()

    sys.exit(app.exec())
