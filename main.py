from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QHBoxLayout, QComboBox, QMessageBox
)
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Приложение управления поставками')
        self.setFixedSize(720, 480)  # Установка фиксированного размера окна

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(QVBoxLayout())

        # Создаем виджет для размещения кнопок
        self.button_widget = QWidget(self)
        self.button_widget.setGeometry(10, 10, 200, 460)  # Устанавливаем координаты и размер для кнопок
        self.button_layout = QVBoxLayout(self.button_widget)

        # Параметры кнопок
        self.create_button('Поставки деталей', self.show_supply_buttons)
        self.create_button('Учёт деталей', self.show_inventory)
        self.create_button('Собрать автомобиль', self.show_assemble_buttons)
        self.create_button('Автомобили', self.show_cars)
        self.create_button('Отчеты', self.show_reports)

        # Правая панель
        self.right_panel = QVBoxLayout()
        self.central_widget.layout().addWidget(self.button_widget)
        self.central_widget.layout().addLayout(self.right_panel)

    def create_button(self, text, callback):
        btn = QPushButton(text, self.button_widget)
        self.button_layout.addWidget(btn)
        btn.clicked.connect(callback)

    def show_supply_buttons(self):
        self.clear_right_panel()
        self.supply_buttons = {
            'Добавить на склад': self.add_to_inventory,
            'Отказ': self.refuse_supply,
            'Добавить поставку': self.add_supply
        }
        for btn_text in self.supply_buttons:
            btn = QPushButton(btn_text)
            btn.clicked.connect(self.supply_buttons[btn_text])
            self.right_panel.addWidget(btn)

    def clear_right_panel(self):
        for i in reversed(range(self.right_panel.count())):
            self.right_panel.itemAt(i).widget().deleteLater()

    def add_to_inventory(self):
        QMessageBox.information(self, 'Добавить на склад', 'Функция "Добавить на склад"')

    def refuse_supply(self):
        QMessageBox.information(self, 'Отказ', 'Функция "Отказ"')

    def add_supply(self):
        self.show_supply_form()

    def show_supply_form(self):
        self.clear_right_panel()
        combo = QComboBox()
        combo.addItems(['Деталь 1', 'Деталь 2', 'Деталь 3'])
        add_btn = QPushButton('Добавить в поставки')
        add_btn.clicked.connect(lambda: self.add_supply_action(combo.currentText()))

        self.right_panel.addWidget(combo)
        self.right_panel.addWidget(add_btn)

    def add_supply_action(self, item):
        QMessageBox.information(self, 'Добавить в поставки', f'Поставлено: {item}')

    def show_assemble_buttons(self):
        self.clear_right_panel()
        fields = [QComboBox() for _ in range(6)]
        for field in fields:
            field.addItems(['Запчасть 1', 'Запчасть 2', 'Запчасть 3'])
            self.right_panel.addWidget(field)

        assemble_btn = QPushButton('Собрать')
        assemble_btn.clicked.connect(lambda: QMessageBox.information(self, 'Собрать', 'Собран автомобиль'))
        self.right_panel.addWidget(assemble_btn)

    def show_inventory(self):
        self.clear_right_panel()
        QMessageBox.information(self, 'Учёт деталей', 'Функция "Учёт деталей"')

    def show_cars(self):
        self.clear_right_panel()
        QMessageBox.information(self, 'Автомобили', 'Функция "Автомобили"')

    def show_reports(self):
        self.clear_right_panel()
        report_btn = QPushButton('Составить отчет')
        report_btn.clicked.connect(lambda: QMessageBox.information(self, 'Отчеты', 'Отчет составлен'))
        self.right_panel.addWidget(report_btn)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
