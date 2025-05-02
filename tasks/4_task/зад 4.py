import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtCore import Qt, QTimer
from Photo import Ui_MainWindow

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main = Ui_MainWindow()
        self.main.setupUi(self)
    def showEvent(self, event):
        super().showEvent(event)
        
        self.i = 0
        self.photoList = [x for x in os.listdir(os.getcwd()) if x.lower().endswith((".jpg", ".jpeg", ".png"))]
        self.dlin = len(self.photoList)
        self.upt()
        self.timer = QTimer()
        self.main.NextButton.clicked.connect(self.next)
        self.main.PrevButton.clicked.connect(self.prev)
        self.main.DeleteButton.clicked.connect(self.delit)
        self.main.StartButton.clicked.connect(self.start)
        self.main.EndButton.clicked.connect(self.end)
        self.main.SShowButton.clicked.connect(self.slideShow)
        self.timer.timeout.connect(self.next)
        self.main.LeftButton.clicked.connect(lambda: self.perev(90))
        self.main.RightButton.clicked.connect(lambda: self.perev(180))
        self.main.SaveButton.clicked.connect(self.Save)

    def scal(self):
        self.scaled = self.pixmap.scaled(self.main.Photo.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.main.Photo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main.Photo.setPixmap(self.scaled)

    def upt(self):
        if self.photoList != [] :
            self.pixmap = QPixmap(self.photoList[self.i])
            self.scal()
            self.check() 
        else:
            self.main.Photo.setStyleSheet("font: 20pt \"Times New Roman\"; ")
            self.main.Photo.setText("Нет изображений :(")
            self.main.PrevButton.setEnabled(False)
            self.main.NextButton.setEnabled(False)
            self.main.SaveButton.setEnabled(False)
            self.main.SShowButton.setEnabled(False)
            self.main.LeftButton.setEnabled(False)
            self.main.RightButton.setEnabled(False)
            self.main.DeleteButton.setEnabled(False)
            self.main.StartButton.setEnabled(False)
            self.main.EndButton.setEnabled(False)
            
            

    def Save(self):
        self.scaled.save(f"{self.photoList[self.i]}")
    def perev(self, id):
        self.pixmap = self.pixmap.transformed(QTransform().rotate(id), Qt.TransformationMode.SmoothTransformation)
        self.scal()
        

    def stopTimer(self):
        self.main.SShowButton.setText("СлайдШоу")
        self.timer.stop()
    
    def slideShow(self):
        if self.timer.isActive():
            self.stopTimer()
        else:
            self.time = int(self.main.comboBox.currentText().split()[0]) * 1000
            self.main.SShowButton.setText("Стоп")
            self.timer.start(self.time)
    
    def start(self):
        self.i = 0
        self.upt()

    def end(self):
        self.i = self.dlin  - 1
        self.upt()
    
    def check(self):
        if self.i == 0:
            self.main.PrevButton.setEnabled(False)
            self.main.NextButton.setEnabled(True)
        elif self.i == self.dlin - 1:
            self.stopTimer()
            self.main.NextButton.setEnabled(False)
            self.main.PrevButton.setEnabled(True)
        else:
            self.main.PrevButton.setEnabled(True)
            self.main.NextButton.setEnabled(True)
        
    def delit(self):
        os.remove(f"{os.getcwd()}/{self.photoList[self.i]}")
        self.photoList.pop(self.i)
        self.photoList = [x for x in os.listdir(os.getcwd()) if x.lower().endswith((".jpg", ".jpeg", ".png"))]
        self.dlin = len(self.photoList)
        if self.i == self.dlin:
            self.i -= 1
        self.upt()

    def prev(self):
        self.i -= 1
        self.upt()

    def next(self):
        self.i += 1
        self.upt()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())