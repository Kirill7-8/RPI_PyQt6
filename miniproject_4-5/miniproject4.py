from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QTabWidget
from PyQt6.QtCore import QSettings
import sys
from proj4 import Ui_MainWindow as Tab
from main import Ui_MainWindow

import json

data = [{"theme1": {
                    "za": ["aaaaaa", "bbbbbb"],
                    "no": ["ccccc", "ddddd"]
                    }}, 
                    {"theme2": {
                        "za": ["12345", "12"],
                        "no": ["no", "yeeeeeeee"]
                    }}]


class proj4(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Tab()
        self.ui.setupUi(self)
        self.upd()

    def upd(self):    
        self.ui.zaList.clear()
        self.ui.zaList.addItems(data[0]["abcd"]["za"])


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.addButton.clicked.connect(self.addTab)
        self.ui.tabs = QTabWidget()
        

    def addTab(self):
        new_tab = proj4()
        tab_index = self.ui.tabWidget.addTab(new_tab, f"Тема {self.ui.tabWidget.count() + 1}")
        self.ui.tabWidget.setCurrentIndex(tab_index)
    
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())