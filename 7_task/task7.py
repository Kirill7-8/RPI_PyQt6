from PyQt6.QtWidgets import QPushButton, QMainWindow, QApplication
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 300)

    def mouseDoubleClickEvent(self, event):
        self.new_btn = QPushButton('click me', self)
        self.new_btn.move(event.pos().x(), event.pos().y())
        self.new_btn.show()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())