from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
from PyQt6.QtCore import QSettings
import sys
from proj3 import Ui_MainWindow
import json

class Project(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.data = QSettings("MyCompany", "App")
        self.data2 = QSettings("Company", "App")
    def showEvent(self, event):
        super().showEvent(event)
        self.curText = ""
        
        self.ui.comboBox.setPlaceholderText("Ваши темы")
        self.ui.labelLine.setPlaceholderText("Поле для аргументов")
        self.ui.zaButton.clicked.connect(self.zaBtn)
        self.ui.noButton.clicked.connect(self.noBtn)
        self.ui.addButton.clicked.connect(self.add)
        self.ui.resetButton.clicked.connect(self.delete)
        self.ui.comboBox.currentTextChanged.connect(self.upt)
        self.ui.upZaButton.clicked.connect(self.upZa)
        self.ui.downZaButton.clicked.connect(self.downZa)
        self.ui.upNoButton.clicked.connect(self.upNo)
        self.ui.downNoButton.clicked.connect(self.downNo)
        self.uptThemes()
        self.upt()

    def downNo(self):
        if self.ui.noList.currentItem():
            lists = self.load_data["no"]
            i = lists.index(self.ui.noList.currentItem().text())
            if self.checkDown(i, lists):
                lists[i], lists[i + 1] = lists[i + 1], lists[i]
                self.load_data["no"] = lists
                self.data.setValue(self.curText, json.dumps(self.load_data))
                self.uptLists()

        
    def upNo(self):
        if self.ui.noList.currentItem():
            lists = self.load_data["no"]
            i = lists.index(self.ui.noList.currentItem().text())
            if self.checkUp(i):
                lists[i], lists[i - 1] = lists[i - 1], lists[i]
                self.load_data["no"] = lists
                self.data.setValue(self.curText, json.dumps(self.load_data))
                self.uptLists()

    def downZa(self):
        if self.ui.zaList.currentItem():
            lists = self.load_data["za"]
            i = lists.index(self.ui.zaList.currentItem().text())
            if self.checkDown(i, lists):
                lists[i], lists[i + 1] = lists[i + 1], lists[i]
                self.load_data["za"] = lists
                self.data.setValue(self.curText, json.dumps(self.load_data))
                self.uptLists()

    def upZa(self):
        if self.ui.zaList.currentItem():
            lists = self.load_data["za"]
            i = lists.index(self.ui.zaList.currentItem().text())
            if self.checkUp(i):
                lists[i], lists[i - 1] = lists[i - 1], lists[i]
                self.load_data["za"] = lists
                self.data.setValue(self.curText, json.dumps(self.load_data))
                self.uptLists()
    
    def checkDown(self, x, listing):
        if x == len(listing) - 1:
            QMessageBox.warning(self, "Ошибка!", "Аргумент и так низший по приоритету!")
            return False
        else:
            return True
    
    def checkUp(self, x):
        if x == 0:
            QMessageBox.warning(self, "Ошибка!", "Аргумент и так высший по приоритету!")
            return False
        else:
            return True
        
    def check(self):
        text = self.ui.labelLine.text().split()
        if self.curText == "" or text == []:
            QMessageBox.warning(self, "Ошибка!", "Поле для ввода аргумента или темы пустое")
            return False
        elif text in self.load_data["za"] or text in self.load_data["no"]:
            QMessageBox.warning(self, "Ошибка!", "Такой аргумент уже есть или поле пустое")
            return False
        else:
            return True
        
    def delete(self):
        if self.curText in (lists := self.data2.value("tasks")):
            self.ui.labelLine.clear()
            lists.remove(self.curText)
            self.data2.setValue("tasks", lists)
            self.data.setValue(self.curText, '{"za": [], "no": []}')
            self.uptLists()
            self.uptThemes()

    def add(self):
        text, ok = QInputDialog.getText(self, "Новое событие", "Введите тему события")
        if ok and text:
            lists = self.data2.value("tasks", [])
            lists.append(text)
            self.data2.setValue("tasks", lists)
            self.data.setValue(text, '{"za": [], "no": []}')
            self.uptThemes()     
            
    def noBtn(self):
        if self.check():
            dicts = self.load_data["no"]
            dicts.append(self.ui.labelLine.text())
            self.load_data["no"] = dicts
            self.data.setValue(self.curText, json.dumps(self.load_data))
            self.uptLists()

    def zaBtn(self):
        if self.check():
            dicts = self.load_data["za"]
            dicts.append(self.ui.labelLine.text())
            self.load_data["za"] = dicts
            self.data.setValue(self.curText, json.dumps(self.load_data))
            self.uptLists()
        
    def upt(self):
        self.curText = self.ui.comboBox.currentText()
        if self.curText:
            self.uptLists()

    def uptLists(self):
        self.ui.zaList.clear()
        self.ui.noList.clear()
        self.load_data = json.loads(self.data.value(self.curText, '{"za": [], "no": []}' ))
        self.ui.lcd1.display(len(self.load_data["za"]))
        self.ui.lcd2.display(len(self.load_data["no"]))
        self.ui.noList.addItems(self.load_data["no"])
        self.ui.zaList.addItems(self.load_data["za"])
            
    def uptThemes(self):
        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(self.data2.value("tasks", []))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Project()
    window.show()
    sys.exit(app.exec())