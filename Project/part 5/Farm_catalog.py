from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPixmap
from ui_farm_catalog import Ui_MainWindow  # Импортируем сгенерированный UI-класс

class ProductCatalog(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Инициализация UI из catalog.ui
        
        # Список товаров
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
        
        self.current_position = 0  # Позиция первого отображаемого товара
        self.products_per_page = 4  # Товаров на странице
        
        # Создаем контейнеры для товаров (адаптируем под ваш дизайн)
        self.create_product_widgets()
        
        # Подключаем кнопки
        self.pushButton.clicked.connect(self.show_previous)
        self.pushButton_2.clicked.connect(self.show_next)
        
        # Первоначальная загрузка товаров
        self.update_products()

    def create_product_widgets(self):
        """Создаем виджеты для отображения товаров"""
        self.product_frames = []
        self.product_images = []
        self.product_names = []
        self.product_prices = []
        self.product_left = []
        self.product_buttons = []
        
        # Создаем стандартный шрифт
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        
        for i in range(self.products_per_page):
            # Фрейм для товара
            frame = QtWidgets.QFrame(parent=self.centralwidget)
            frame.setGeometry(QtCore.QRect(20 + (i%2)*220, 60 + (i//2)*290, 200, 280))
            frame.setStyleSheet("""
                background-color: white;
                border-radius: 10px;
                padding: 10px;
                font-family: Arial;
            """)
            frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            
            # Изображение товара
            image = QtWidgets.QLabel(parent=frame)
            image.setGeometry(QtCore.QRect(10, 20, 180, 180))
            image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            
            # Название товара
            name = QtWidgets.QLabel(parent=frame)
            name.setGeometry(QtCore.QRect(10, 10, 180, 40))
            name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            name.setStyleSheet("""
                font-weight: bold; 
                font-size: 10pt;
                font-family: Arial;
            """)
            
            # Цена товара
            price = QtWidgets.QLabel(parent=frame)
            price.setGeometry(QtCore.QRect(0, 230, 100, 50))
            price.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            price.setStyleSheet("""
                color: #2c3e50; 
                font-size: 11pt;
                font-family: Arial;
            """)
            
            # Количество оставшегося товара
            left = QtWidgets.QLabel(parent=frame)
            left.setGeometry(QtCore.QRect(10, 198, 180, 50))
            left.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            left.setStyleSheet("""
                font-weight: bold; 
                font-size: 10pt;
                font-family: Arial;
            """)
            
            # Кнопка заказа
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
                
            # Сохраняем ссылки
            self.product_frames.append(frame)
            self.product_images.append(image)
            self.product_names.append(name)
            self.product_prices.append(price)
            self.product_left.append(left)
            self.product_buttons.append(order_btn)

    def update_products(self):
        """Обновляем отображаемые товары"""
        for i in range(self.products_per_page):
            product_index = self.current_position + i
            
            if product_index < len(self.products):
                product = self.products[product_index]
                
                # Показываем фрейм и заполняем данными
                self.product_frames[i].show()
                self.product_names[i].setText(product["name"])
                self.product_prices[i].setText(f"Цена: {product['price']}")
                self.product_left[i].setText(f"Осталось {product["left"]}шт")
                
                # Загружаем изображение (путь должен быть правильным)
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
                # Скрываем фрейм, если товара нет
                self.product_frames[i].hide()

    def show_previous(self):
        """Показывает предыдущие 4 товара"""
        if self.current_position >= self.products_per_page:
            self.current_position -= self.products_per_page
            self.update_products()

    def show_next(self):
        """Показывает следующие 4 товара"""
        if self.current_position + self.products_per_page < len(self.products):
            self.current_position += self.products_per_page
            self.update_products()

# Запуск приложения
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ProductCatalog()
    window.setWindowTitle("Каталог лекарств")
    window.show()
    sys.exit(app.exec())