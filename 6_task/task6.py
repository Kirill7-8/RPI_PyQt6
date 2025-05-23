from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from Login import Ui_LoginWindow
from PyQt6.QtCore import QSettings
from Reg import Ui_Form
import sys
import re
import hashlib
import json


def hashPas(x):
    return hashlib.sha256(x.encode()).hexdigest()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)


        self.i = None
        self.flag = False
        self.pas = None
        self.logins = set()
        self.emails = set()
        self.nums = set()
        self.data = QSettings("MyCompany", "App")
        self.loaded = json.loads(self.data.value("users", '{"users": []}'))

        self.loadedData = self.loaded["users"]
        
        if self.loadedData:
            self.logins = {x["login"] for x in self.loadedData}
            self.emails = {x["email"] for x in self.loadedData}
            self.nums = {x["phone"] for x in self.loadedData}

        self.initUI()

    def initUI(self):
        self.ui.logLine.setPlaceholderText("Введите логин")
        self.ui.regButton.clicked.connect(self.show_registration)
        self.ui.logLine.editingFinished.connect(self.logCheck)
        self.ui.pasLine.editingFinished.connect(self.pasCheck)
        self.ui.logButton.clicked.connect(self.log)

    def log(self):

        if self.flag and self.i is not None:
            user = self.loadedData[self.i]

            QMessageBox.information(self,
                                    f"Поздравляем! {user["fio"]}",
                                    f"Пользователь c логином: {user["login"]} успешно вошел в систему!\n"
                                    f"Номером: {user["phone"]}\n"
                                    f"Почтой: {user["email"]}\n"
                                    f"О себе: {user["about"]}")
        else:
            QMessageBox.warning(self, "Внимание!", "Не все поля заполнены!!")
            self.ui.pasLine.clear()

    def pasCheck(self):
        
        if self.pas:
            if self.pas == hashPas(self.ui.pasLine.text()):
                self.flag = True
            else:
                QMessageBox.warning(self, "Внимание!", "Неверный пароль!")
                self.ui.pasLine.clear()

    def logCheck(self):

        log = self.ui.logLine.text()

        for user in self.loadedData:
            if log in self.logins:
                if log in user["login"]:
                    self.i = user["id"]
                    self.pas = user["password"]
            else:
                QMessageBox.warning(self, "Внимание!", "Пользователь не найден!")
                self.ui.logLine.clear()

    def show_registration(self):
        self.registration_window = RegistrationWindow(
            logins=self.logins,
            emails=self.emails,
            nums=self.nums,
            data=self.data,
            loaded=self.loaded,
            loadedData=self.loadedData
        )
        self.registration_window.show()
        self.hide()


class RegistrationWindow(QWidget):
    def __init__(self, logins, emails, nums, data, loaded, loadedData):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        

        self.logins = logins
        self.emails = emails
        self.nums = nums
        self.data = data
        self.loaded = loaded
        self.loadedData = loadedData
        
        self.initUI()


        self.about = None
        self.city = None
        self.login = None
        self.pas = None
        self.pas2 = None
        self.email = None
        self.num = None
        self.fio = ""

        
        
    def initUI(self):
        self.ui.fioLine.setPlaceholderText("ФИО")
        self.ui.cityLine.setPlaceholderText("Город")
        self.ui.loginLine.setPlaceholderText("Придумайте логин")
        self.ui.pasLine.setPlaceholderText("Придумайте пароль")
        self.ui.pas2Line.setPlaceholderText("Повторите пароль")
        self.ui.emailLine.setPlaceholderText("Почта")
        self.ui.numLine.setInputMask("Номер Телефона: +7 - 999 - 999 - 99 - 99")
        self.ui.aboutLine.setPlaceholderText("Расскажите о себе")

        self.ui.cityLine.editingFinished.connect(self.checkCity)
        self.ui.aboutLine.editingFinished.connect(self.checkAbout)
        self.ui.fioLine.editingFinished.connect(self.checkFio)
        self.ui.loginLine.editingFinished.connect(self.checkLog)
        self.ui.pasLine.editingFinished.connect(self.checkPas)
        self.ui.pas2Line.editingFinished.connect(self.checkPas2)
        self.ui.numLine.editingFinished.connect(self.checkNum)
        self.ui.emailLine.editingFinished.connect(self.checkEmail)

        self.ui.regButton.clicked.connect(self.reg)

    def checkCity(self):
        self.city = self.ui.cityLine.text().capitalize()

    def checkAbout(self):
        self.about = self.ui.aboutLine.text()
   

    def loadData(self):
        i = 0
        Data = {"id": None,
                "login": self.login,
                "phone": self.num,
                "email": self.email,
                "password": self.pas,
                "fio": self.fio,
                "city": self.city,
                "about": self.about}
        
        for d in self.loadedData:
            if d["id"] == i:
                i += 1

        Data["id"] = i
        self.loadedData.append(Data)
        self.data.setValue("users", json.dumps(self.loaded))

    def checkFio(self):
        self.fio = self.ui.fioLine.text().title()

    def reg(self):
        flag = self.login is not None and self.pas is not None and self.pas2 is not None and self.email is not None and self.num is not None
        if flag:
            QMessageBox.information(self, f"Поздравляем! {self.fio}", f"Пользователь c логином: {self.login} успешно зарегистрирован!\n"
                                                                      f"Номером: {self.num}\n"
                                                                      f"Почтой: {self.email}")
            self.loadData()

        else:
            QMessageBox.warning(self, "Неудача", "Не все обязательные поля заполнены!\n* - обязательные поля")

    def checkEmail(self):
        if not re.match(r"[A-Za-z0-9._%+-]+@[A-Za-z]+\.[A-Za-z]{2,}", self.ui.emailLine.text()):
            QMessageBox.warning(self, "Внимание!", "Введите правильную электронную почту!\nexample123@example.ru/com")
        elif self.ui.emailLine.text() in self.emails:
            QMessageBox.warning(self, "Внимание!", "Такая почта уже зарегистрирована!")
            self.ui.emailLine.clear()
        else:
            self.email = self.ui.emailLine.text()


    def checkNum(self):
        self.num = "".join(self.ui.numLine.text().split(" - "))[16:]
        if self.num in self.nums:
            QMessageBox.warning(self, "Внимание!", "Такой номер телефона уже зарегистрирован!")
            self.ui.numLine.clear()

    def checkPas2(self):
        if self.pas is not None:
            pas2 = self.ui.pas2Line.text()
            if self.pas == hashPas(pas2):
                self.pas2 = hashPas(pas2)
            else:
                QMessageBox.warning(self, "Внимание!", "Пароли не совпадают!")
        else:
            QMessageBox.warning(self, "Внимание!", "Сначала заполните предыдущее поле!")

    def checkLog(self):
        if not re.match(r"^[a-zA-Z0-9]{5,}$", self.ui.loginLine.text()):
            QMessageBox.warning(self, "Некорректный логин!", "Логин должен состоять не менее чем из 5\nсимволов из набора латинского алфавита или цифр")
        elif self.ui.loginLine.text() in self.logins:
            QMessageBox.warning(self, "Внимание!", "Такой логин уже зарегистрирован!")
            self.ui.loginLine.clear()
        else:
            self.login = self.ui.loginLine.text()

    def checkPas(self):
        pas = self.ui.pasLine.text()
        if len(pas) < 8:
            QMessageBox.warning(self, "Некорректный пароль!", "Длина пароля должна быть не менее 8 символов!")
        elif re.match(r"(.*[а-я][А-Я])", pas):
            QMessageBox.warning(self, "Некорректный пароль!", "В пароле не должно быть кириллицы!")
        elif not re.match(r"(.*[A-Z])", pas):
            QMessageBox.warning(self, "Некорректный пароль!", "В пароле должна быть хотя бы одна строчная буква\nиз латинского алфавита!")
        elif not re.match(r"(.*[a-z])", pas):
            QMessageBox.warning(self, "Некорректный пароль!", "В пароле должна быть хотя бы одна прописная буква\nиз латинского алфавита!")
        elif not re.match(r"(.*[0-9])", pas):
            QMessageBox.warning(self, "Некорректный пароль!", "В пароле должны быть хотя бы одна цифра!")
        elif not re.match(r"(.*\W)", pas):
            QMessageBox.warning(self, "Некорректный пароль!", "В пароле должны быть хотя бы один специальный символ!")
        else:
            self.pas = hashPas(pas)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())