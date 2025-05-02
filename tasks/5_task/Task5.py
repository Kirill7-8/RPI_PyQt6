import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Task5.ui', self)


        self.flag = False
        self.orderButton.setEnabled(self.flag)
        self.orderButton.clicked.connect(self.end)
        self.label.setText("      Выберите \nминимум 2 блюда!")

        self.firstButton.clicked.connect(self.btn)
        self.soup1.clicked.connect(lambda: self.btn(1))
        self.soup2.clicked.connect(lambda: self.btn(1))
        self.soup3.clicked.connect(lambda: self.btn(1))

        self.secondButton.clicked.connect(self.btn)
        self.second1.clicked.connect(lambda: self.btn(2))
        self.second2.clicked.connect(lambda: self.btn(2))
        self.second3.clicked.connect(lambda: self.btn(2))

        self.saladButton.clicked.connect(self.btn)
        self.salad1.clicked.connect(lambda: self.btn(3))
        self.salad3.clicked.connect(lambda: self.btn(3))
        self.salad2.clicked.connect(lambda: self.btn(4))

        self.drinkButton.clicked.connect(self.btn)
        self.drink1.clicked.connect(lambda: self.btn(5))
        self.drink2.clicked.connect(lambda: self.btn(5))
        self.drink3.clicked.connect(lambda: self.btn(5))

        self.desertButton.clicked.connect(lambda: self.btn(6))
        self.desert1.clicked.connect(lambda: self.btn(6))
        self.desert2.clicked.connect(lambda: self.btn(6))


    def btn(self, id):
        
        second = (self.second1.isChecked() + self.second2.isChecked() + self.second3.isChecked())
        first = (self.soup1.isChecked() + self.soup2.isChecked() + self.soup3.isChecked())
        desert = (self.desert1.isChecked() + self.desert2.isChecked())
        drink = (self.drink1.isChecked() + self.drink2.isChecked() + self.drink3.isChecked())
        salad = (self.salad1.isChecked() + self.salad2.isChecked() + self.salad3.isChecked())
        a = (self.firstButton.isChecked() + self.secondButton.isChecked() + self.saladButton.isChecked() +
             self.drinkButton.isChecked() + self.desertButton.isChecked())
        flag1 = a >= 2
        flag2 = (first + second + desert + drink + salad) >= 2
        if flag1 and flag2:
            self.flag = True
        else:
            self.flag = False
        self.orderButton.setEnabled(self.flag)
    def end(self):
        QMessageBox.information(self, "Ура!", "Заказ принят!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
