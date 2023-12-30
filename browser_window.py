# browser_windows.py
from PyQt5.QtCore import QUrl, Qt, QPoint
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QMenu, QToolButton, QSystemTrayIcon, QAction, QMessageBox

from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setUrl(QUrl("http://www.google.com"))
        self.loadFinished.connect(self.load_finished)
        self.loadProgress.connect(self.load_progress)

    def load_finished(self, ok):
        if not ok:
            error_message = "Failed to load the page. Please check your internet connection or try again later."
            QMessageBox.critical(None, "Error", error_message, QMessageBox.Ok)

    def load_progress(self, progress):
        if progress == 100:
            self.parent().statusBar().clearMessage()
        else:
            self.parent().statusBar().showMessage(f"Loading... {progress}%")

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.draggable = True
        self.old_pos = None

        self.browser = Browser()
        self.browser.urlChanged.connect(self.update_urlbar)

        nav_toolbar = QToolBar("Navigation")
        self.addToolBar(Qt.TopToolBarArea, nav_toolbar)
        nav_toolbar.setMovable(False)  # Запрет перемещения ToolBar

        # Добавленные отступы слева
        left_margin = 10
        nav_toolbar.setContentsMargins(left_margin, 0, 0, 0)

        # Add navigation buttons
        back_btn = QAction("Back", self)
        back_btn.setStatusTip("Go back to the previous page")
        back_btn.triggered.connect(self.browser.back)  
        nav_toolbar.addAction(back_btn)

        forward_btn = QAction("Forward", self)
        forward_btn.setStatusTip("Forward to the next page")
        forward_btn.triggered.connect(self.browser.forward)  
        nav_toolbar.addAction(forward_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)  
        nav_toolbar.addAction(reload_btn)

        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        nav_toolbar.addAction(home_btn)

        nav_toolbar.addSeparator()

        # Address/Search bar
        self.urlbar = QLineEdit()
        self.urlbar.setPlaceholderText("Search on Google")
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        nav_toolbar.addWidget(self.urlbar)

        # Control buttons
        control_menu = QMenu("Control", self)
        close_action = control_menu.addAction("Close", self.close_browser)
        close_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q))  

        full_action = control_menu.addAction("Full-screen", self.toggle_full_screen)
        full_action.setShortcut(QKeySequence(Qt.Key_F11))

        control_btn = QToolButton()
        control_btn.setMenu(control_menu)
        control_btn.setPopupMode(QToolButton.InstantPopup)

        nav_toolbar.addWidget(control_btn)

        # System tray icon
        tray_icon = QSystemTrayIcon(QIcon(), self)  
        tray_icon.setToolTip("Simple Browser")
        tray_icon.activated.connect(self.tray_icon_activated)

        # Optimization: enable caching
        self.browser.page().profile().setHttpCacheType(2)  

        # Remove the standard window control panel
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Show the icon in the system tray
        tray_icon.show()

        # Apply styles from the styles.css file
        style_file = "styles.css"
        with open(style_file, "r") as f:
            self.setStyleSheet(f.read())

        # Configure the main window
        self.setWindowTitle("Simple Browser")
        self.setGeometry(100, 100, 800, 600)

        # Set the browser in the central area of the window
        self.setCentralWidget(self.browser)
        
    def update_urlbar(self, q):
        # Получаем текущий URL и обновляем содержимое строки urlbar
        self.urlbar.setText(q.toString())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.draggable:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        query = self.urlbar.text().strip()

        if query:
            # Construct the Google search URL
            google_search_url = f"https://www.google.com/search?q={query}"
            self.browser.setUrl(QUrl(google_search_url))

    def close_browser(self):
        self.close()

    def toggle_full_screen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.showNormal()

    def load_finished(self, ok):
        if not ok:
            error_message = "Failed to load the page. Please check your internet connection or try again later."
            QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)

    def load_progress(self, progress):
        if progress == 100:
            self.statusBar().clearMessage()
        else:
            self.statusBar().showMessage(f"Loading... {progress}%")

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName("Simple Browser")

    window = BrowserWindow()
    window.show()

    sys.exit(app.exec())
