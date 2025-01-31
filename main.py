import sys
import psycopg2
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox,
    QDialog, QComboBox, QListWidgetItem, QSpinBox, QInputDialog, QStackedWidget, QDateEdit, QSpacerItem, QSizePolicy, QTableWidgetItem, QTableWidget
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QDate


class WarehouseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Система управления поставками')
        self.setGeometry(300, 300, 800, 600)
        self.connection = self.connect_db()
        self.initUI()
        self.load_supplies()

    def connect_db(self):
        try:
            return psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="Kosmostars1234",
                host="localhost"
            )
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка подключения', str(e))
            sys.exit(-1)

    def initUI(self):
        main_layout = QHBoxLayout()
        # Левая панель с кнопками
        left_panel = QVBoxLayout()
        self.supply_button = QPushButton('Поставки деталей', self)
        self.supply_button.clicked.connect(self.show_supply_page)
        left_panel.addWidget(self.supply_button)
        self.inventory_button = QPushButton('Учёт деталей', self)
        self.inventory_button.clicked.connect(self.show_inventory_page)
        left_panel.addWidget(self.inventory_button)
        self.assemble_button = QPushButton('Собрать автомобиль', self)
        self.assemble_button.clicked.connect(self.show_assemble_page)
        left_panel.addWidget(self.assemble_button)
        self.cars_button = QPushButton('Автомобили', self)
        self.cars_button.clicked.connect(self.show_cars_page)
        left_panel.addWidget(self.cars_button)
        self.reports_button = QPushButton('Отчеты', self)
        self.reports_button.clicked.connect(self.show_reports_page)
        left_panel.addWidget(self.reports_button)
        main_layout.addLayout(left_panel)
        # Страницы для различных функций
        self.stacked_widget = QStackedWidget(self)
        # Страница для поставок деталей
        self.supply_page = QWidget()
        self.supply_page_layout = QVBoxLayout()
        self.supply_list = QListWidget(self)
        self.supply_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.supply_page_layout.addWidget(self.supply_list)
        self.create_supply_button = QPushButton('Создать поставку', self)
        self.create_supply_button.clicked.connect(self.open_supply_dialog)
        self.supply_page_layout.addWidget(self.create_supply_button)
        self.edit_supply_button = QPushButton('Редактировать поставку', self)
        self.edit_supply_button.clicked.connect(self.edit_selected_supply)
        self.supply_page_layout.addWidget(self.edit_supply_button)
        self.remove_supply_button = QPushButton('Отказаться от поставки', self)
        self.remove_supply_button.clicked.connect(self.remove_selected_supply)
        self.supply_page_layout.addWidget(self.remove_supply_button)
        self.add_to_storage_button = QPushButton('Внести на склад', self)
        self.add_to_storage_button.clicked.connect(self.add_to_storage)
        self.supply_page_layout.addWidget(self.add_to_storage_button)
        self.supply_page.setLayout(self.supply_page_layout)
        self.stacked_widget.addWidget(self.supply_page)
        # Страница для учета деталей
        self.inventory_page = QWidget()
        self.inventory_page_layout = QVBoxLayout()
        self.storage_combo = QComboBox(self)
        self.inventory_page_layout.addWidget(QLabel('Выберите склад:'))
        self.inventory_page_layout.addWidget(self.storage_combo)
        self.storage_combo.currentIndexChanged.connect(self.load_storage_contents)
        self.storage_contents_list = QListWidget(self)
        self.inventory_page_layout.addWidget(self.storage_contents_list)
        self.inventory_page.setLayout(self.inventory_page_layout)
        self.stacked_widget.addWidget(self.inventory_page)
        # Страница для сборки автомобилей
        self.assemble_page = QWidget()
        self.assemble_page_layout = QVBoxLayout()

        # Вертикальный макет для основного содержимого страницы
        main_content_layout = QVBoxLayout()

        # Поле для ввода даты
        self.date_edit = QDateEdit(self)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setMaximumWidth(200)  # Ограничиваем ширину поля для ввода даты

        # Центральный макет для поля ввода даты
        date_layout = QHBoxLayout()
        date_layout.addStretch(1)
        date_layout.addWidget(QLabel('Выберите дату создания автомобиля:'))
        date_layout.addWidget(self.date_edit)
        date_layout.addStretch(1)
        main_content_layout.addLayout(date_layout)

        assemble_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Добавление полей со списком слева
        self.engine_combo = QComboBox(self)
        left_layout.addWidget(QLabel('Двигатель:'))
        left_layout.addWidget(self.engine_combo)
        self.suspension_combo = QComboBox(self)
        left_layout.addWidget(QLabel('Подвеска:'))
        left_layout.addWidget(self.suspension_combo)
        self.transmission_combo = QComboBox(self)
        left_layout.addWidget(QLabel('Трансмиссия:'))
        left_layout.addWidget(self.transmission_combo)

        # Центральная картинка
        pixmap = QPixmap('C:\\Users\\user\\Desktop\\zadankya\\TimeForCode\\images.jpeg')  # Замените на путь к вашей картинке
        image_label = QLabel(self)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Добавление полей со списком справа
        self.wheels_combo = QComboBox(self)
        right_layout.addWidget(QLabel('Колеса:'))
        right_layout.addWidget(self.wheels_combo)
        self.body_combo = QComboBox(self)
        right_layout.addWidget(QLabel('Кузов:'))
        right_layout.addWidget(self.body_combo)
        self.gearbox_combo = QComboBox(self)
        right_layout.addWidget(QLabel('Коробка передач:'))
        right_layout.addWidget(self.gearbox_combo)

        assemble_layout.addLayout(left_layout)
        assemble_layout.addWidget(image_label)
        assemble_layout.addLayout(right_layout)

        # Добавляем все элементы в основной макет
        main_content_layout.addLayout(assemble_layout)

        # Кнопка "Собрать автомобиль" переносится в самый низ
        self.assemble_button = QPushButton('Собрать автомобиль', self)
        self.assemble_button.clicked.connect(self.assemble_car)
        main_content_layout.addWidget(self.assemble_button)  # Кнопка добавляется в самый низ

        self.assemble_page_layout.addLayout(main_content_layout)
        self.assemble_page.setLayout(self.assemble_page_layout)
        self.stacked_widget.addWidget(self.assemble_page)

        # Страница для автомобилей
        self.cars_page = QWidget()
        self.cars_page_layout = QVBoxLayout()
        self.car_table = QTableWidget(self)
        self.car_table.setColumnCount(8)
        self.car_table.setHorizontalHeaderLabels(
            ['ID', 'Дата создания', 'Двигатель', 'Колеса', 'Трансмиссия', 'Кузов', 'Подвеска', 'Коробка передач'])
        self.cars_page_layout.addWidget(self.car_table)
        self.cars_page.setLayout(self.cars_page_layout)
        self.stacked_widget.addWidget(self.cars_page)

        # Страница для отчетов
        self.reports_page = QWidget()
        self.reports_page_layout = QVBoxLayout()
        self.daily_report_button = QPushButton('Отчет за день', self)
        self.daily_report_button.clicked.connect(self.show_daily_report)
        self.reports_page_layout.addWidget(self.daily_report_button)
        self.weekly_report_button = QPushButton('Отчет за неделю', self)
        self.weekly_report_button.clicked.connect(self.show_weekly_report)
        self.reports_page_layout.addWidget(self.weekly_report_button)
        self.monthly_report_button = QPushButton('Отчет за месяц', self)
        self.monthly_report_button.clicked.connect(self.show_monthly_report)
        self.reports_page_layout.addWidget(self.monthly_report_button)
        self.report_table = QTableWidget(self)
        self.report_table.setColumnCount(2)
        self.report_table.setHorizontalHeaderLabels(['Дата', 'Количество автомобилей'])
        self.reports_page_layout.addWidget(self.report_table)
        self.reports_page.setLayout(self.reports_page_layout)
        self.stacked_widget.addWidget(self.reports_page)

        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)
        self.load_storages()
        self.load_parts_comboboxes()

    def load_supplies(self):
        self.supply_list.clear()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT id, дата_создания FROM Поставки")
            for row in cursor.fetchall():
                self.supply_list.addItem(f'Поставка ID: {row[0]}, Дата: {row[1]}')

    def open_supply_dialog(self):
        self.supply_dialog = SupplyDialog(self)
        self.supply_dialog.exec()
        self.load_supplies()

    def edit_selected_supply(self):
        selected_items = self.supply_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Ошибка', 'Выберите поставку для редактирования.')
            return
        supply_item = selected_items[0]
        supply_id_text = supply_item.text()
        try:
            self.current_supply_id = int(supply_id_text.split(',')[0].split(':')[1].strip())
        except ValueError as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка извлечения ID: {str(e)}')
            return
        self.supply_dialog = SupplyDialog(self, self.current_supply_id)
        self.supply_dialog.exec()
        self.load_supplies()

    def remove_selected_supply(self):
        selected_items = self.supply_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Ошибка', 'Выберите поставку для удаления.')
            return
        supply_item = selected_items[0]
        supply_id_text = supply_item.text()
        try:
            supply_id = int(supply_id_text.split(',')[0].split(':')[1].strip())
        except ValueError as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка извлечения ID: {str(e)}')
            return
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM Поставка_Запчасти WHERE поставка_id = %s", (supply_id,))
                cursor.execute("DELETE FROM Поставки WHERE id = %s", (supply_id,))
                self.connection.commit()
                QMessageBox.information(self, 'Успех', 'Поставка успешно удалена.')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось удалить поставку: {str(e)}')
            self.connection.rollback()
        self.load_supplies()

    def add_to_storage(self):
        selected_items = self.supply_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Ошибка', 'Выберите поставку для добавления на склад.')
            return
        supply_item = selected_items[0]
        supply_id_text = supply_item.text()
        try:
            supply_id = int(supply_id_text.split(',')[0].split(':')[1].strip())
        except ValueError as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка извлечения ID: {str(e)}')
            return
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT запчасть_id, количество, тип_запчасти FROM Поставка_Запчасти WHERE поставка_id = %s",
                    (supply_id,)
                )
                parts = cursor.fetchall()
                for part_id, quantity, part_type in parts:
                    cursor.execute(f"SELECT количество FROM склад_{part_type} WHERE id = %s", (part_id,))
                    result = cursor.fetchone()
                    if result:  # Если запчасть уже на складе, обновляем количество
                        new_quantity = result[0] + quantity
                        cursor.execute(
                            f"UPDATE склад_{part_type} SET количество = %s WHERE id = %s",
                            (new_quantity, part_id)
                        )
                    else:  # Если запчасть отсутствует на складе, добавляем новую запись
                        cursor.execute(
                            f"INSERT INTO склад_{part_type} (id, название, количество) "
                            f"SELECT id, название, %s FROM {part_type} WHERE id = %s",
                            (quantity, part_id)
                        )
                self.connection.commit()
                QMessageBox.information(self, 'Успех', 'Запчасти успешно внесены на склад.')
                # Удаление поставки из базы данных
                cursor.execute("DELETE FROM Поставка_Запчасти WHERE поставка_id = %s", (supply_id,))
                cursor.execute("DELETE FROM Поставки WHERE id = %s", (supply_id,))
                self.connection.commit()
                # Обновление списка поставок в интерфейсе
                self.load_supplies()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось внести запчасти на склад: {str(e)}')
            self.connection.rollback()

    def show_supply_page(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_inventory_page(self):
        self.stacked_widget.setCurrentIndex(1)
        self.load_storages()

    def show_assemble_page(self):
        self.stacked_widget.setCurrentIndex(2)

    def show_cars_page(self):
        self.stacked_widget.setCurrentIndex(3)
        self.load_car_table()

    def show_reports_page(self):
        self.stacked_widget.setCurrentIndex(4)

    def load_storages(self):
        self.storage_combo.clear()
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'склад_%'")
            storages = [row[0] for row in cursor.fetchall()]
            for storage in storages:
                self.storage_combo.addItem(storage)

    def load_storage_contents(self):
        selected_storage = self.storage_combo.currentText()
        self.storage_contents_list.clear()
        if selected_storage:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {selected_storage}")
                columns = [desc[0] for desc in cursor.description]
                contents = cursor.fetchall()
                for row in contents:
                    item_text = ', '.join([f'{col}: {val}' for col, val in zip(columns, row)])
                    self.storage_contents_list.addItem(item_text)

    def load_parts_comboboxes(self):
        with self.connection.cursor() as cursor:
            # Загрузка двигателей
            cursor.execute("SELECT id, название FROM двигатели")
            engines = cursor.fetchall()
            for engine in engines:
                self.engine_combo.addItem(engine[1], engine[0])
            # Загрузка подвесок
            cursor.execute("SELECT id, название FROM подвески")
            suspensions = cursor.fetchall()
            for suspension in suspensions:
                self.suspension_combo.addItem(suspension[1], suspension[0])
            # Загрузка трансмиссий
            cursor.execute("SELECT id, название FROM трансмиссии")
            transmissions = cursor.fetchall()
            for transmission in transmissions:
                self.transmission_combo.addItem(transmission[1], transmission[0])
            # Загрузка колес
            cursor.execute("SELECT id, название FROM колеса")
            wheels = cursor.fetchall()
            for wheel in wheels:
                self.wheels_combo.addItem(wheel[1], wheel[0])
            # Загрузка кузовов
            cursor.execute("SELECT id, название FROM кузова")
            bodies = cursor.fetchall()
            for body in bodies:
                self.body_combo.addItem(body[1], body[0])
            # Загрузка коробок передач
            cursor.execute("SELECT id, название FROM коробки_передач")
            gearboxes = cursor.fetchall()
            for gearbox in gearboxes:
                self.gearbox_combo.addItem(gearbox[1], gearbox[0])

    def assemble_car(self):
        engine_id = self.engine_combo.currentData()
        suspension_id = self.suspension_combo.currentData()
        transmission_id = self.transmission_combo.currentData()
        wheels_id = self.wheels_combo.currentData()
        body_id = self.body_combo.currentData()
        gearbox_id = self.gearbox_combo.currentData()

        if not all([engine_id, suspension_id, transmission_id, wheels_id, body_id, gearbox_id]):
            QMessageBox.warning(self, 'Ошибка', 'Выберите все запчасти для сборки автомобиля.')
            return

        try:
            with self.connection.cursor() as cursor:
                # Проверяем наличие запчастей на складах
                cursor.execute("SELECT количество FROM склад_двигатели WHERE id = %s", (engine_id,))
                engine_row = cursor.fetchone()
                if engine_row is None or engine_row[0] < 1:
                    QMessageBox.warning(self, 'Ошибка', 'Недостаточно двигателей на складе.')
                    return
                engine_quantity = engine_row[0]

                cursor.execute("SELECT количество FROM склад_подвески WHERE id = %s", (suspension_id,))
                suspension_row = cursor.fetchone()
                if suspension_row is None or suspension_row[0] < 1:
                    QMessageBox.warning(self, 'Ошибка', 'Недостаточно подвесок на складе.')
                    return
                suspension_quantity = suspension_row[0]

                cursor.execute("SELECT количество FROM склад_трансмиссии WHERE id = %s", (transmission_id,))
                transmission_row = cursor.fetchone()
                if transmission_row is None or transmission_row[0] < 1:
                    QMessageBox.warning(self, 'Ошибка', 'Недостаточно трансмиссий на складе.')
                    return
                transmission_quantity = transmission_row[0]

                cursor.execute("SELECT количество FROM склад_колеса WHERE id = %s", (wheels_id,))
                wheels_row = cursor.fetchone()
                if wheels_row is None or wheels_row[0] < 1:
                    QMessageBox.warning(self, 'Ошибка', 'Недостаточно колес на складе.')
                    return
                wheels_quantity = wheels_row[0]

                cursor.execute("SELECT количество FROM склад_кузова WHERE id = %s", (body_id,))
                body_row = cursor.fetchone()
                if body_row is None or body_row[0] < 1:
                    QMessageBox.warning(self, 'Ошибка', 'Недостаточно кузовов на складе.')
                    return
                body_quantity = body_row[0]

                cursor.execute("SELECT количество FROM склад_коробки_передач WHERE id = %s", (gearbox_id,))
                gearbox_row = cursor.fetchone()
                if gearbox_row is None or gearbox_row[0] < 1:
                    QMessageBox.warning(self, 'Ошибка', 'Недостаточно коробок передач на складе.')
                    return
                gearbox_quantity = gearbox_row[0]

                # Уменьшаем количество запчастей на складах
                cursor.execute("UPDATE склад_двигатели SET количество = количество - 1 WHERE id = %s", (engine_id,))
                cursor.execute("UPDATE склад_подвески SET количество = количество - 1 WHERE id = %s", (suspension_id,))
                cursor.execute("UPDATE склад_трансмиссии SET количество = количество - 1 WHERE id = %s",
                               (transmission_id,))
                cursor.execute("UPDATE склад_колеса SET количество = количество - 1 WHERE id = %s", (wheels_id,))
                cursor.execute("UPDATE склад_кузова SET количество = количество - 1 WHERE id = %s", (body_id,))
                cursor.execute("UPDATE склад_коробки_передач SET количество = количество - 1 WHERE id = %s",
                               (gearbox_id,))

                # Создаем запись в таблице собранных автомобилей
                car_creation_date = self.date_edit.date().toString(
                    "yyyy-MM-dd")  # Получаем выбранную дату или текущую дату
                cursor.execute(
                    "INSERT INTO собранные_автомобили (дата_создания, двигатель, колеса, трансмиссия, кузов, подвеска, коробка_передач) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;",
                    (car_creation_date, engine_id, wheels_id, transmission_id, body_id, suspension_id, gearbox_id)
                )
                car_id = cursor.fetchone()[0]

                self.connection.commit()
                QMessageBox.information(self, 'Успех', 'Автомобиль успешно собран.')

                # Обновляем таблицу собранных автомобилей
                self.load_car_table()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Произошла ошибка при сборке автомобиля: {str(e)}')
            self.connection.rollback()

    def load_car_table(self):
        self.car_table.setRowCount(0)
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, дата_создания, 
                       (SELECT название FROM двигатели WHERE id = собранные_автомобили.двигатель),
                       (SELECT название FROM колеса WHERE id = собранные_автомобили.колеса),
                       (SELECT название FROM трансмиссии WHERE id = собранные_автомобили.трансмиссия),
                       (SELECT название FROM кузова WHERE id = собранные_автомобили.кузов),
                       (SELECT название FROM подвески WHERE id = собранные_автомобили.подвеска),
                       (SELECT название FROM коробки_передач WHERE id = собранные_автомобили.коробка_передач)
                FROM собранные_автомобили
            """)
            cars = cursor.fetchall()
            for row_number, car in enumerate(cars):
                self.car_table.insertRow(row_number)
                for column_number, data in enumerate(car):
                    self.car_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def show_daily_report(self):
        self.load_report('day')

    def show_weekly_report(self):
        self.load_report('week')

    def show_monthly_report(self):
        self.load_report('month')

    def load_report(self, period):
        self.report_table.setRowCount(0)
        with self.connection.cursor() as cursor:
            if period == 'day':
                query = """
                    SELECT DATE(дата_создания) AS date, COUNT(*) AS count
                    FROM собранные_автомобили
                    WHERE DATE(дата_создания) = CURRENT_DATE
                    GROUP BY DATE(дата_создания)
                """
            elif period == 'week':
                query = """
                    SELECT DATE(дата_создания) AS date, COUNT(*) AS count
                    FROM собранные_автомобили
                    WHERE DATE(дата_создания) >= CURRENT_DATE - INTERVAL '7 days'
                    GROUP BY DATE(дата_создания)
                """
            elif period == 'month':
                query = """
                    SELECT DATE(дата_создания) AS date, COUNT(*) AS count
                    FROM собранные_автомобили
                    WHERE DATE(дата_создания) >= CURRENT_DATE - INTERVAL '1 month'
                    GROUP BY DATE(дата_создания)
                """
            else:
                return

            cursor.execute(query)
            reports = cursor.fetchall()
            for row_number, report in enumerate(reports):
                self.report_table.insertRow(row_number)
                for column_number, data in enumerate(report):
                    self.report_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


class SupplyDialog(QDialog):
    def __init__(self, parent=None, supply_id=None):
        super().__init__(parent)
        self.setWindowTitle('Создание/Редактирование поставки')
        self.parent = parent
        self.supply_id = supply_id
        self.temp_supplies = []
        self.layout = QVBoxLayout()
        self.part_type_combo = QComboBox(self)
        self.part_type_combo.addItems(['двигатели', 'колеса', 'кузова', 'коробки_передач', 'трансмиссии', 'подвески'])
        self.part_type_combo.currentIndexChanged.connect(self.load_parts)
        self.layout.addWidget(QLabel('Выберите тип запчасти:'))
        self.layout.addWidget(self.part_type_combo)
        self.part_combo = QComboBox(self)
        self.layout.addWidget(QLabel('Выберите запчасть:'))
        self.layout.addWidget(self.part_combo)
        self.quantity_input = QSpinBox(self)
        self.layout.addWidget(QLabel('Введите количество:'))
        self.layout.addWidget(self.quantity_input)
        self.add_button = QPushButton('Добавить', self)
        self.add_button.clicked.connect(self.add_part)
        self.layout.addWidget(self.add_button)
        self.current_parts_list = QListWidget(self)
        self.layout.addWidget(QLabel('Внесенные запчасти:'))
        self.layout.addWidget(self.current_parts_list)
        self.finalize_button = QPushButton('Создать/Обновить поставку', self)
        self.finalize_button.clicked.connect(self.finalize_supply)
        self.layout.addWidget(self.finalize_button)
        self.setLayout(self.layout)
        if self.supply_id:
            self.load_current_supply()
            self.load_parts()

    def load_parts(self):
        self.part_combo.clear()
        part_type = self.part_type_combo.currentText()
        with self.parent.connection.cursor() as cursor:
            cursor.execute(f"SELECT id, название FROM {part_type}")
            parts = cursor.fetchall()
            for part in parts:
                self.part_combo.addItem(f'{part[1]} (ID: {part[0]})', userData=part[0])

    def load_current_supply(self):
        if not self.supply_id:
            return
        try:
            with self.parent.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT запчасть_id, количество, тип_запчасти FROM Поставка_Запчасти WHERE поставка_id = %s",
                    (self.supply_id,)
                )
                current_parts = cursor.fetchall()
                for part_id, quantity, part_type in current_parts:
                    self.temp_supplies.append((part_id, quantity, part_type))
                    self.current_parts_list.addItem(f'{part_type} (ID: {part_id}), Количество: {quantity}')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить информацию о поставке: {str(e)}')

    def add_part(self):
        part_id = self.part_combo.currentData()
        quantity = self.quantity_input.value()
        if quantity <= 0:
            QMessageBox.warning(self, 'Ошибка', 'Количество должно быть больше 0.')
            return
        part_type = self.part_type_combo.currentText()
        self.temp_supplies.append((part_id, quantity, part_type))
        self.current_parts_list.addItem(f'{part_type} (ID: {part_id}), Количество: {quantity}')
        self.quantity_input.setValue(0)

    def finalize_supply(self):
        if not self.temp_supplies:
            QMessageBox.warning(self, 'Ошибка', 'Нет запчастей для добавления в поставку.')
            return
        try:
            with self.parent.connection.cursor() as cursor:
                if not self.supply_id:
                    cursor.execute("INSERT INTO Поставки (дата_создания) VALUES (CURRENT_TIMESTAMP) RETURNING id;")
                    new_supply_id = cursor.fetchone()[0]
                    for part_id, quantity, part_type in self.temp_supplies:
                        # Проверяем, существует ли запись
                        cursor.execute(
                            "SELECT COUNT(*) FROM Поставка_Запчасти WHERE поставка_id = %s AND запчасть_id = %s AND тип_запчасти = %s",
                            (new_supply_id, part_id, part_type)
                        )
                        exists = cursor.fetchone()[0]
                        if exists:
                            # Если запись существует, обновляем количество
                            cursor.execute(
                                "UPDATE Поставка_Запчасти SET количество = количество + %s WHERE поставка_id = %s AND запчасть_id = %s AND тип_запчасти = %s",
                                (quantity, new_supply_id, part_id, part_type)
                            )
                        else:
                            # Если записи нет, добавляем новую
                            cursor.execute(
                                "INSERT INTO Поставка_Запчасти (поставка_id, запчасть_id, количество, тип_запчасти) VALUES (%s, %s, %s, %s)",
                                (new_supply_id, part_id, quantity, part_type)
                            )
                    self.parent.connection.commit()
                    QMessageBox.information(self, 'Успех', 'Поставка успешно создана.')
                else:
                    cursor.execute("DELETE FROM Поставка_Запчасти WHERE поставка_id = %s", (self.supply_id,))
                    for part_id, quantity, part_type in self.temp_supplies:
                        # Повторная проверка для обновления
                        cursor.execute(
                            "SELECT COUNT(*) FROM Поставка_Запчасти WHERE поставка_id = %s AND запчасть_id = %s AND тип_запчасти = %s",
                            (self.supply_id, part_id, part_type)
                        )
                        exists = cursor.fetchone()[0]
                        if exists:
                            cursor.execute(
                                "UPDATE Поставка_Запчасти SET количество = количество + %s WHERE поставка_id = %s AND запчасть_id = %s AND тип_запчасти = %s",
                                (quantity, self.supply_id, part_id, part_type)
                            )
                        else:
                            cursor.execute(
                                "INSERT INTO Поставка_Запчасти (поставка_id, запчасть_id, количество, тип_запчасти) VALUES (%s, %s, %s, %s)",
                                (self.supply_id, part_id, quantity, part_type)
                            )
                    self.parent.connection.commit()
                    QMessageBox.information(self, 'Успех', 'Поставка успешно обновлена.')
            self.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Произошла ошибка при сохранении: {str(e)}')
            self.parent.connection.rollback()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WarehouseApp()
    ex.show()
    sys.exit(app.exec())