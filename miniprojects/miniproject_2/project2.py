from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import QSettings
from PyQt6 import uic
import sys
class Project(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = QSettings("MyCompany", "App")
        uic.loadUi('miniproject2.ui', self)
        self.ZaButton.clicked.connect(self.zaBtn)
        self.NoButton.clicked.connect(self.noBtn)
        self.ResetButton.clicked.connect(self.reset)
        self.LabelLine.setPlaceholderText("Помощник в принятии решений ver. 2")
        self.VoiceLine.setPlaceholderText("Ваш аргумент")
        self.upt()
    def reset(self):
        self.VoiceLine.clear()
        self.ZaList.clear()
        self.NoList.clear()
        self.LabelLine.clear()
        self.data.setValue("Text", "")
        self.data.setValue("Za", [])
        self.data.setValue("No", [])
        self.upt()

    def noBtn(self):
        No = self.data.value("No", [])
        noLine = self.VoiceLine.text()
        if noLine == "" or self.LabelLine.text() == "":
            QMessageBox.warning(self, "Ошибка!", "Поле для ввода аргумента пустое")
        elif (noLine in No) or (noLine in self.data.value("Za", [])):
            QMessageBox.warning(self, "Ошибка!", "Такой аргумент уже есть!")
        else:
            No = self.data.value("No", [])
            No.append(noLine)
            self.data.setValue("No", No)
            self.upt()
    def upt(self):
        self.ZaButton.setText(f"За!\n{len(self.data.value("Za", []))}")
        self.NoButton.setText(f"Против!\n{len(self.data.value("No", []))}")
        self.ZaList.clear()
        self.NoList.clear()
        self.ZaList.addItems(self.data.value("Za",[]))
        self.NoList.addItems(self.data.value("No",[]))
        if self.LabelLine.text() != "":
            self.data.setValue("Text", self.LabelLine.text())
        self.LabelLine.setText(self.data.value("Text"))


    def zaBtn(self):
        Za = self.data.value("Za", [])
        zaLine = self.VoiceLine.text()
        if zaLine == "" or self.LabelLine.text() == "":
            QMessageBox.warning(self, "Ошибка!", "Поле для ввода аргумента пустое")
        elif (zaLine in Za) or (zaLine in self.data.value("No", [])):
            QMessageBox.warning(self, "Ошибка!", "Такой аргумент уже есть!")
        else:
            Za.append(zaLine)
            self.data.setValue("Za", Za)
            self.upt()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Project()
    window.show()
    sys.exit(app.exec())