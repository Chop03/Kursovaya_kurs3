import sys
import psycopg2
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
    QDialog,
    QFormLayout,
    QSpinBox,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QDialogButtonBox,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Детали Автомобилей")
        self.setGeometry(100, 100, 800, 600)

        # Подключение к базе данных PostgreSQL
        try:
            self.connection = psycopg2.connect(
                dbname="postgres",
                user="postgres",  # Замените на ваше имя пользователя
                password="Kosmostars1234",  # Замените на ваш пароль
                host="localhost",
                port="5432",
            )
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            sys.exit(1)

            # Основной виджет и макет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        # Создание виджета с вертикальными вкладками
        self.tab_list = QListWidget()
        self.tab_list.addItems(["Поставки деталей", "Учет деталей", "Собрать автомобиль", "Автомобили", "Отчеты"])
        self.tab_list.currentItemChanged.connect(self.change_tab)

        # Стacked widget для содержимого вкладок
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.tab_list)
        self.layout.addWidget(self.stacked_widget)

        # Добавление вкладок с их содержимым
        self.create_tabs()

        self.show()

    def create_tabs(self):
        # Вкладка "Поставки деталей"
        self.tab_supply_details = QWidget()
        self.create_supply_details_tab(self.tab_supply_details)
        self.stacked_widget.addWidget(self.tab_supply_details)

        # Остальные вкладки (пока пустые)
        for tab_name in ["Учет деталей", "Собрать автомобиль", "Автомобили", "Отчеты"]:
            self.stacked_widget.addWidget(QWidget())  # Пустая вкладка

    def create_supply_details_tab(self, tab):
        main_layout = QHBoxLayout(tab)

        # Левый box для поставок
        left_box = QWidget()
        left_layout = QVBoxLayout(left_box)
        self.supply_list = QListWidget()
        self.supply_list.addItems([
            "Кузова",
            "Моторы",
            "Трансмиссии",
            "Коробки передач",
            "Колеса",
            "Подвески"
        ])
        self.supply_list.currentItemChanged.connect(self.display_supply_details)
        left_layout.addWidget(self.supply_list)

        # Правый box для деталей поставки
        right_box = QWidget()
        right_layout = QVBoxLayout(right_box)
        self.details_label = QLabel("Выберите поставку для отображения деталей")
        right_layout.addWidget(self.details_label)

        self.details_box = QListWidget()
        right_layout.addWidget(self.details_box)

        # Кнопки
        button_layout = QVBoxLayout()
        self.add_supply_button = QPushButton("Добавить поставку")
        self.add_supply_button.clicked.connect(self.open_add_supply_dialog)
        reject_button = QPushButton("Отказ")
        reject_button.clicked.connect(self.reject_supply)

        button_layout.addWidget(self.add_supply_button)
        button_layout.addWidget(reject_button)

        main_layout.addWidget(left_box)
        main_layout.addWidget(right_box)
        main_layout.addLayout(button_layout)

    def open_add_supply_dialog(self):
        dialog = AddSupplyDialog(self)
        dialog.exec()

    def display_supply_details(self):
        current_supply = self.supply_list.currentItem()
        if current_supply:
            supply_name = current_supply.text().replace(" ", "_")  # Для правильного имени таблицы
            self.details_label.setText(f"Детали для {supply_name}:")
            self.load_parts(supply_name)

    def load_parts(self, supply_name):
        self.details_box.clear()
        # Загрузка деталей для выбранной поставки
        # Реализуйте логику загрузки деталей здесь

    def reject_supply(self):
        current_supply = self.supply_list.currentItem()
        if current_supply:
            supply_name = current_supply.text().replace(" ", "_")  # Для правильного имени таблицы
            try:
                delete_query = f"DELETE FROM {supply_name};"  # Измените на нужный запрос
                self.cursor.execute(delete_query)
                self.connection.commit()
                QMessageBox.information(self, "Успех", f"Поставка {supply_name} очищена.")
                self.supply_list.takeItem(self.supply_list.currentRow())  # Удалить предмет из списка
            except Exception as e:
                print(f"Ошибка при сбросе поставки {supply_name}: {e}")

    def change_tab(self, current: QListWidgetItem):
        if current:
            index = self.tab_list.row(current)
            self.stacked_widget.setCurrentIndex(index)

    def closeEvent(self, event):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        event.accept()


class AddSupplyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить поставку")

        # Таблица для деталей
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Деталь", "Количество"])

        # Комбобокс для выбора склада
        self.warehouse_combo = QComboBox()
        self.warehouse_combo.addItems([
            "Склад кузовов",
            "Склад двигателей",
            "Склад колес",
            "Склад подвесок",
            "Склад трансмиссий",
            "Склад коробок передач"
        ])

        # Кнопки
        self.add_button = QPushButton("Добавить в поставки")
        self.add_button.clicked.connect(self.add_supply)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.table)
        self.layout.addWidget(QLabel("Выберите склад:"))
        self.layout.addWidget(self.warehouse_combo)
        self.layout.addWidget(self.add_button)

        self.table.setRowCount(1)  # Начальное количество строк

    def add_supply(self):
        # Логика для добавления поставки
        rows = self.table.rowCount()
        warehouse = self.warehouse_combo.currentText().replace("Склад ", "").replace(" ",
                                                                                     "_")  # Убираем "Склад " и пробелы для имени таблицы

        for row in range(rows):
            part_name_item = self.table.item(row, 0)
            quantity_item = self.table.item(row, 1)
            if part_name_item and quantity_item:
                part_name = part_name_item.text()
                quantity = quantity_item.text()
                if part_name and quantity.isdigit() and int(quantity) > 0:
                    self.insert_supply_to_db(part_name, int(quantity), warehouse)

        self.close()  # Закрываем диалог после добавления

    def insert_supply_to_db(self, part_name, quantity, warehouse):
        try:
            insert_query = f"INSERT INTO {warehouse} (name, quantity) VALUES (%s, %s);"
            self.parent().cursor.execute(insert_query, (part_name, quantity))
            self.parent().connection.commit()
            QMessageBox.information(self, "Успех", "Поставка добавлена.")
            self.parent().supply_list.addItem(f"{part_name} - {quantity}")  # Обновляем список поставок в главном окне
        except Exception as e:
            print(f"Ошибка при добавлении поставки: {e}")
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить поставку в базу данных.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())  
