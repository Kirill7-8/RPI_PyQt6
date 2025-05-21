from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QTabWidget, QInputDialog
from Login import Ui_LoginWindow
from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QPixmap
from PyQt6 import QtCore, QtGui, QtWidgets
from Reg import Ui_Form
import sys
import re
import hashlib
from ui_farm_catalog import Ui_MainWindow as Farm_catalog
from ui_user_catalog import Ui_MainWindow as User_catalog
import json

class Farm_cat(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Farm_catalog()
        self.ui.setupUi(self)
        self.products = [
            {"name": "Аспирин", "price": "99 ₽", "image": "aspirin.jpg", "left": 1},
            {"name": "АЦЦ", "price": "149 ₽", "image": "ACC.jpg", "left": 4},
            {"name": "Амоксиклав", "price": "709 ₽", "image": "amoksiklav.jpg", "left": 5},
            {"name": "Кардио магнил", "price": "189 ₽", "image": "cardio magnil.jpg", "left": 10},
            {"name": "Цитрамон", "price": "59 ₽", "image": "citramon.jpg", "left": 6},
            {"name": "Анальгин", "price": "49 ₽", "image": "analgin.jpg", "left": 9},
            {"name": "Корвалол", "price": "129 ₽", "image": "corvalol.jpg", "left": 4},
            {"name": "Валидол", "price": "89 ₽", "image": "validol.jpg", "left": 5}
        ]
        
        self.current_position = 0  
        self.products_per_page = 4 
        
        self.create_product_widgets()
        
        self.ui.pushButton.clicked.connect(self.show_previous)
        self.ui.pushButton_2.clicked.connect(self.show_next)
        self.ui.pushButton_3.clicked.connect(self.show_base)
        self.ui.pushButton_4.deleteLater()

        self.update_products()
    def show_base(self):
        text = ""
        for k in range(len(self.products)):
            text = text + f"\n{self.products[k]["name"].ljust(20)} | {self.products[k]["price"].ljust(6)} | {str(self.products[k]["left"]).ljust(3)}шт"
        print(text)
        QtWidgets.QMessageBox.information(
            self, 
            "База Данных", 
            text
        )

    def order_product(self, product_index):
        actual_index = self.current_position + product_index
        if actual_index < len(self.products):
            product = self.products[actual_index]
            QtWidgets.QMessageBox.information(
                self, 
                "Заказ", 
                f"Название: {product['name']}\nЦена: {product['price']}\nВ ожидании оплаты..."
            )
    def create_product_widgets(self):
        self.product_frames = []
        self.product_images = []
        self.product_names = []
        self.product_prices = []
        self.product_left = []
        self.product_buttons = []
        
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        
        for i in range(self.products_per_page):
            frame = QtWidgets.QFrame(parent=self.ui.centralwidget)
            frame.setGeometry(QtCore.QRect(20 + (i%2)*220, 60 + (i//2)*290, 200, 280))
            frame.setStyleSheet("""
                background-color: white;
                border-radius: 10px;
                padding: 10px;
                font-family: Arial;
            """)
            frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            
            image = QtWidgets.QLabel(parent=frame)
            image.setGeometry(QtCore.QRect(10, 20, 180, 180))
            image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
            name = QtWidgets.QLabel(parent=frame)
            name.setGeometry(QtCore.QRect(10, 10, 180, 40))
            name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            name.setStyleSheet("""
                font-weight: bold; 
                font-size: 10pt;
                font-family: Arial;
            """)
    
            price = QtWidgets.QLabel(parent=frame)
            price.setGeometry(QtCore.QRect(0, 230, 100, 50))
            price.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            price.setStyleSheet("""
                color: #2c3e50; 
                font-size: 11pt;
                font-family: Arial;
            """)
    
            left = QtWidgets.QLabel(parent=frame)
            left.setGeometry(QtCore.QRect(10, 198, 180, 50))
            left.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            left.setStyleSheet("""
                font-weight: bold; 
                font-size: 10pt;
                font-family: Arial;
            """)
            
            order_btn = QtWidgets.QPushButton("Заказать", parent=frame)
            order_btn.setGeometry(QtCore.QRect(100, 240, 100, 35))
            order_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 11pt;
                    font-family: Arial;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            order_btn.clicked.connect(lambda _, idx=i: self.order_product(idx))
            self.product_frames.append(frame)
            self.product_images.append(image)
            self.product_names.append(name)
            self.product_prices.append(price)
            self.product_left.append(left)
            self.product_buttons.append(order_btn)

    def update_products(self):
        for i in range(self.products_per_page):
            product_index = self.current_position + i
            
            if product_index < len(self.products):
                product = self.products[product_index]
                
                self.product_frames[i].show()
                self.product_names[i].setText(product["name"])
                self.product_prices[i].setText(f"Цена: {product['price']}")
                self.product_left[i].setText(f"Осталось {product["left"]}шт")

                
                pixmap = QPixmap(f"images/{product['image']}")
                if not pixmap.isNull():
                    self.product_images[i].setPixmap(
                        pixmap.scaled(140, 140, 
                                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                    QtCore.Qt.TransformationMode.SmoothTransformation)
                    )
                else:
                    self.product_images[i].setText("Нет изображения")
            else:
                self.product_frames[i].hide()

    def show_previous(self):
        if self.current_position >= self.products_per_page:
            self.current_position -= self.products_per_page
            self.update_products()

    def show_next(self):
        if self.current_position + self.products_per_page < len(self.products):
            self.current_position += self.products_per_page
            self.update_products()

class User_cat(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = User_catalog()
        self.ui.setupUi(self)
        self.products = [
            {"name": "Аспирин", "price": "99 ₽", "image": "aspirin.jpg", "left": 1},
            {"name": "АЦЦ", "price": "149 ₽", "image": "ACC.jpg", "left": 4},
            {"name": "Амоксиклав", "price": "709 ₽", "image": "amoksiklav.jpg", "left": 5},
            {"name": "Кардио магнил", "price": "189 ₽", "image": "cardio magnil.jpg", "left": 10},
            {"name": "Цитрамон", "price": "59 ₽", "image": "citramon.jpg", "left": 6},
            {"name": "Анальгин", "price": "49 ₽", "image": "analgin.jpg", "left": 9},
            {"name": "Корвалол", "price": "129 ₽", "image": "corvalol.jpg", "left": 4},
            {"name": "Валидол", "price": "89 ₽", "image": "validol.jpg", "left": 5}
        ]
        
        self.current_position = 0  
        self.products_per_page = 4  
        
        self.create_product_widgets()

        self.ui.pushButton.clicked.connect(self.show_previous)
        self.ui.pushButton_2.clicked.connect(self.show_next)
        self.ui.pushButton_3.deleteLater()
        
        self.update_products()

    def create_product_widgets(self):
        self.product_frames = []
        self.product_images = []
        self.product_names = []
        self.product_prices = []
        self.product_left = []
        self.product_buttons = []
        
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        
        for i in range(self.products_per_page):
            frame = QtWidgets.QFrame(parent=self.ui.centralwidget)
            frame.setGeometry(QtCore.QRect(20 + (i%2)*220, 60 + (i//2)*290, 200, 280))
            frame.setStyleSheet("""
                background-color: white;
                border-radius: 10px;
                padding: 10px;
                font-family: Arial;
            """)
            frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            
            image = QtWidgets.QLabel(parent=frame)
            image.setGeometry(QtCore.QRect(10, 20, 180, 180))
            image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
            name = QtWidgets.QLabel(parent=frame)
            name.setGeometry(QtCore.QRect(10, 10, 180, 40))
            name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            name.setStyleSheet("""
                font-weight: bold; 
                font-size: 10pt;
                font-family: Arial;
            """)
    
            price = QtWidgets.QLabel(parent=frame)
            price.setGeometry(QtCore.QRect(0, 230, 100, 50))
            price.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            price.setStyleSheet("""
                color: #2c3e50; 
                font-size: 11pt;
                font-family: Arial;
            """)
    
            left = QtWidgets.QLabel(parent=frame)
            left.setGeometry(QtCore.QRect(10, 198, 180, 50))
            left.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            left.setStyleSheet("""
                font-weight: bold; 
                font-size: 10pt;
                font-family: Arial;
            """)
            
            order_btn = QtWidgets.QPushButton("Заказать", parent=frame)
            order_btn.setGeometry(QtCore.QRect(100, 240, 100, 35))
            order_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 11pt;
                    font-family: Arial;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            order_btn.clicked.connect(lambda _, idx=i: self.order_product(idx))

            self.product_frames.append(frame)
            self.product_images.append(image)
            self.product_names.append(name)
            self.product_prices.append(price)
            self.product_left.append(left)
            self.product_buttons.append(order_btn)
    
    def order_product(self, product_index):
        actual_index = self.current_position + product_index
        if actual_index < len(self.products):
            product = self.products[actual_index]
            QtWidgets.QMessageBox.information(
                self, 
                "Заказ", 
                f"Вы заказали: {product['name']}\nЦена: {product['price']}"
            )

    def update_products(self):
        for i in range(self.products_per_page):
            product_index = self.current_position + i
            
            if product_index < len(self.products):
                product = self.products[product_index]
                
                self.product_frames[i].show()
                self.product_names[i].setText(product["name"])
                self.product_prices[i].setText(f"Цена: {product['price']}")
                self.product_left[i].setText(f"Осталось {product["left"]}шт")

                
                pixmap = QPixmap(f"images/{product['image']}")
                if not pixmap.isNull():
                    self.product_images[i].setPixmap(
                        pixmap.scaled(140, 140, 
                                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                    QtCore.Qt.TransformationMode.SmoothTransformation)
                    )
                else:
                    self.product_images[i].setText("Нет изображения")
            else:
                self.product_frames[i].hide()

    def show_previous(self):
        if self.current_position >= self.products_per_page:
            self.current_position -= self.products_per_page
            self.update_products()

    def show_next(self):
        if self.current_position + self.products_per_page < len(self.products):
            self.current_position += self.products_per_page
            self.update_products()


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
        self.upd()

        print(self.loadedData)
        

        self.initUI()                        

    def upd(self):
        self.loaded = json.loads(self.data.value("users", '{"users": []}'))
        self.loadedData = self.loaded["users"]
        if self.loadedData:
            self.logins = {x["login"] for x in self.loadedData}
            self.emails = {x["email"] for x in self.loadedData}
            self.nums = {x["phone"] for x in self.loadedData}


    def initUI(self):
        self.ui.logLine.setPlaceholderText("Введите логин")
        self.ui.regButton.clicked.connect(self.show_registration)
        self.ui.logLine.editingFinished.connect(self.logCheck)
        self.ui.pasLine.editingFinished.connect(self.pasCheck)
        self.ui.logButton.clicked.connect(self.log)

    def log(self):
        if self.flag and self.i is not None:
            self.show_helper()
        else:
            QMessageBox.warning(self, "Внимание!", "Не все поля заполнены!!")
            self.ui.pasLine.clear()
                                      
    def show_helper(self):
        if "Farm" in self.ui.logLine.text():
            self.main = Farm_cat()
        else:
            self.main = User_cat()
        self.main.show()
        self.hide()

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
            self.upd()
            if log in self.logins:
                if log in user["login"]:
                    self.i = user["id"]
                    self.pas = user["password"]
            else:
                self.upd()
                QMessageBox.warning(self, "Внимание!", "Пользователь не найден!")
                self.ui.logLine.clear()
                break

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
            
            main_window.show()
            self.hide()

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