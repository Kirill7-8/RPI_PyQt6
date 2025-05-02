import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import QSettings
class Voiting(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.data = QSettings("data", "Voit")
        self.app()

    def app(self):
        self.clik1 = self.data.value("да", 0, type=int)
        self.clik2 = self.data.value("нет", 0, type=int)

        self.setWindowTitle("Помощник в принятии решений")
        self.resize(500, 300)
        self.setStyleSheet("background-color: #C0C0C0")

        self.za = QtWidgets.QPushButton(f"За!\n{self.clik1}", self)
        self.za.resize(150, 75)
        self.za.move((self.width() // 10), (self.height() // 2) - (self.za.height() // 2))
        self.za.clicked.connect(self.cliker1)
        self.za.setStyleSheet("""
            QPushButton {
                    background-color: #1E90FF;
                    color: black;
                }
                }
            QPushButton:pressed {
                    background-color: #3df205;
                }
            """)

        self.no = QtWidgets.QPushButton(f"Против!\n{self.clik2}", self)
        self.no.resize(150, 75)
        self.no.move(self.width() - (self.width() // 10) - self.no.width(),
                     (self.height() // 2) - (self.za.height() // 2))
        self.no.clicked.connect(self.cliker2)
        self.no.setStyleSheet("""
                    QPushButton {
                            background-color: #1E90FF;
                            color: black;
                        }
                        }
                    QPushButton:pressed {
                            background-color: #FF0000;
                        }
                    """)

        self.res = QtWidgets.QPushButton("Сбросить результаты голования", self)
        self.res.resize(180, 60)
        self.res.move((self.width() - self.res.width()) // 2, self.height() - (self.height() // 3))
        self.res.clicked.connect(self.reset)
        self.res.setStyleSheet("""
            QPushButton {
                            background-color: #1E90FF;
                            color: black;
                        }
                        }
                    QPushButton:pressed {
                            background-color: orange;
                        }
            """)
        self.show()

    def cliker1(self):
        self.clik1 += 1
        self.data.setValue("да", self.clik1)
        self.za.setText(f"За!\n{self.clik1}")
    def cliker2(self):
        self.clik2 += 1
        self.data.setValue("нет", self.clik2)
        self.no.setText(f"Против!\n{self.clik2}")
    def reset(self):
        self.clik1 = 0
        self.clik2 = 0
        self.data.setValue("да", self.clik1)
        self.data.setValue("нет", self.clik2)
        self.za.setText(f"За!\n{self.clik1}")
        self.no.setText(f"Против!\n{self.clik2}")


app = QtWidgets.QApplication(sys.argv)
window = Voiting()
sys.exit(app.exec())
