import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox
from PyQt6.QtCore import QSettings, QDate
class DailyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = QSettings("MyCompany", "App")
        uic.loadUi('3task.ui', self)
        self.calendarWidget.setMinimumDate(QDate.currentDate())
        self.events = self.data.value("datas", [])
        self.addButton.clicked.connect(self.AddBtn)
        self.Upt()
        self.listWidget.itemDoubleClicked.connect(self.Delete)

    def Delete(self, item):
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            f"Завершить событие: {item.text()}?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            row = self.listWidget.row(item)
            self.listWidget.takeItem(row)
            self.events.pop(row)
            self.data.setValue("datas", self.events)

    def Upt(self):
        self.listWidget.clear()
        if self.data.value("datas", []) != []:
            for d in self.data.value("datas"):
                self.listWidget.addItem(f"{d["name"]} {d["time"]} {d["date"]}")
                


    def AddBtn(self):
        text, ok = QInputDialog.getText(self, "Новое событие", "Что планируете?", text="Ничего")
        if ok and text:
            event = {
                "name": text,
                "date": self.calendarWidget.selectedDate().toString("dd.MM.yyyy"),
                "time": self.timeEdit.time().toString("HH:mm")
            }
            self.events.append(event)
            self.events.sort(key=lambda x: (x["date"], x["time"]))
            self.data.setValue("datas", self.events)
            self.Upt()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DailyApp()
    window.show()
    sys.exit(app.exec())
