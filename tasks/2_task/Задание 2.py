import sys
from PyQt6 import QtWidgets


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        self.k = 0
        super().__init__()
        self.setWindowTitle("MyFirstApp")
        self.resize(300, 300)
        self.label = QtWidgets.QLabel("Попробуй нажать!", self)
        self.btn = QtWidgets.QPushButton("Прямо на меня", self)
        self.btn.resize(100, 30)
        self.btny = ((self.height() - self.btn.height()) // 2)
        self.label.move((self.width() - self.label.width()) // 2, self.btny - self.btn.height())
        self.btn.move((self.width() - self.btn.width()) // 2, self.btny)
        self.btn.clicked.connect(self.mot)
        self.btncnt = QtWidgets.QPushButton(f"Тапай меня!\nНатапано: {self.k}", self)
        self.btncnt.move((self.width() // 5) - (self.btncnt.width() // 2), 0)
        self.btncnt.clicked.connect(self.klik)

        self.labYN = QtWidgets.QLabel("2 + 2 = 4!?", self)
        self.labYN.resize(150,30)
        self.labYN.move((self.width() // 2) - (self.labYN.width() // 4), 0)
        self.bY = QtWidgets.QPushButton("ДА!", self)
        self.bN = QtWidgets.QPushButton("НЕТ!", self)
        self.bY.resize(50, 20)
        self.bN.resize(50, 20)
        self.bY.move((self.width() // 2) - (self.bY.width()), self.labYN.height())
        self.bN.move((self.width() // 2), self.labYN.height())
        self.bN.clicked.connect(self.YN)
        self.bY.clicked.connect(self.YN)

        self.mybut = QtWidgets.QPushButton("Сброс", self)
        self.mybut.resize(50,20)
        self.mybut.clicked.connect(self.sbros)
        self.mybut.move((self.width() - (self.width() // 5)) - (self.mybut.width() // 4), 0)

        self.help = QtWidgets.QPushButton("Подсказка!", self)
        self.help.resize(self.bY.width() + self.bN.width(),self.labYN.height())
        self.help.clicked.connect(self.YN)
        self.help.move((self.width() // 2) - (self.help.width() // 2), self.labYN.height() + self.bY.height())
        self.show()
    def sbros(self):
        self.k = 0
        self.btncnt.setText(f"Тапай меня!\nНатапано: {self.k}")
        self.labYN.setText("2 + 2 = 4!?")
        self.btn.move((self.width() - self.btn.width()) // 2, self.btny)

    def mot(self):
        y = self.btn.y()
        if self.btn.x() == self.width() - self.btn.width():
            self.btn.move(-50, y)
        self.btn.move(self.btn.x() + 50, y)
    def klik(self):
        self.k += 1
        self.btncnt.setText(f"Тапай меня!\nНатапано: {self.k}")
    def YN(self):
        if self.sender() == self.bY:
            self.labYN.setText("2 + 2 = 4!?\nНет! Не верно!")
        elif self.sender() == self.help:
            self.labYN.setText("2 + 2 = 4!?\n4! = 1 * 2 * 3 * 4 = 24")
        else:
            self.labYN.setText("2 + 2 = 4!?\nДа! Верно")

app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
sys.exit(app.exec())