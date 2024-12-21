import dearpygui.dearpygui as dpg
import json
from transport import Client, Vehicle, TransportCompany, Van, Airplane

company = TransportCompany("My transport company") # Глобальные переменные для хранения данных


# Функции для обновления таблиц
def update_clients_table():
    dpg.delete_item("clients_table", children_only=True)  # Удаляем все строки из таблицы клиентов
    for client in company.clients:
        with dpg.table_row(parent="clients_table"):  # Добавляем новую строку в таблицу клиентов
            dpg.add_text(client.name)  # Добавляем имя клиента
            dpg.add_text(str(client.cargo_weight))  # Добавляем вес груза клиента
            dpg.add_text("Да" if client.is_vip else "Нет")  # Добавляем статус VIP клиента (Да/Нет)

def update_vehicles_table():
    dpg.delete_item("vehicles_table", children_only=True)  # Удаляем все строки из таблицы транспортных средств
    for vehicle in company.vehicles:
        with dpg.table_row(parent="vehicles_table"):  # Добавляем новую строку в таблицу транспортных средств
            dpg.add_text(str(vehicle.vehicle_id))  # Добавляем ID транспортного средства
            dpg.add_text(str(vehicle.capacity))  # Добавляем грузоподъёмность транспортного средства
            dpg.add_text(str(vehicle.current_load))  # Добавляем текущую загрузку транспортного средства
            if isinstance(vehicle, Airplane):
                dpg.add_text(f"Высота: {vehicle.max_altitude}")  # Если транспортное средство - самолёт, добавляем максимальную высоту полета
            elif isinstance(vehicle, Van):
                dpg.add_text(f"Холодильник: {'Да' if vehicle.is_refrigerated else 'Нет'}")  # Если транспортное средство - фургон, добавляем информацию о наличии холодильника


def show_all_clients():
    if dpg.does_item_exist("all_clients_window"):  # Проверяем, существует ли окно "all_clients_window"
        return
    with dpg.window(label="Все клиенты", modal=True, width=600, height=400, tag="all_clients_window"):  # Создаем новое окно "Все клиенты"
        with dpg.table(header_row=True):  # Создаем таблицу с заголовком
            dpg.add_table_column(label="Имя клиента")  # Добавляем колонку "Имя клиента"
            dpg.add_table_column(label="Вес груза")  # Добавляем колонку "Вес груза"
            dpg.add_table_column(label="VIP статус")  # Добавляем колонку "VIP статус"
            for client in company.clients:
                with dpg.table_row():  # Добавляем строку в таблицу для каждого клиента
                    dpg.add_text(client.name)  # Добавляем имя клиента
                    dpg.add_text(str(client.cargo_weight))  # Добавляем вес груза клиента
                    dpg.add_text("Да" if client.is_vip else "Нет")  # Добавляем статус VIP клиента (Да/Нет)
        dpg.add_button(label="Закрыть", callback=lambda: dpg.delete_item("all_clients_window"))  # Добавляем кнопку "Закрыть" для удаления окна



def show_all_vehicles():
    if dpg.does_item_exist("all_vehicles_window"):  # Проверяем, существует ли окно "all_vehicles_window"
        return
    with dpg.window(label="Все транспортные средства", modal=True, width=700, height=500, tag="all_vehicles_window"):  # Создаем новое окно "Все транспортные средства"
        with dpg.table(header_row=True):  # Создаем таблицу с заголовком
            dpg.add_table_column(label="ID")  # Добавляем колонку "ID"
            dpg.add_table_column(label="Грузоподъемность")  # Добавляем колонку "Грузоподъемность"
            dpg.add_table_column(label="Текущая загрузка")  # Добавляем колонку "Текущая загрузка"
            dpg.add_table_column(label="Особенности")  # Добавляем колонку "Особенности"
            for vehicle in company.vehicles:
                with dpg.table_row():  # Добавляем строку в таблицу для каждого транспортного средства
                    dpg.add_text(str(vehicle.vehicle_id))  # ID транспортного средства
                    dpg.add_text(str(vehicle.capacity))  # Грузоподъемность
                    dpg.add_text(str(vehicle.current_load))  # Текущая загрузка
                    if isinstance(vehicle, Airplane):
                        dpg.add_text(f"Высота: {vehicle.max_altitude}")  # Если транспортное средство - самолёт, добавляем максимальную высоту полета
                    elif isinstance(vehicle, Van):
                        dpg.add_text(f"Холодильник: {'Да' if vehicle.is_refrigerated else 'Нет'}")  # Если транспортное средство - фургон, добавляем информацию о наличии холодильника
        dpg.add_button(label="Закрыть", callback=lambda: dpg.delete_item("all_vehicles_window"))  # Добавляем кнопку "Закрыть" для удаления окна

def show_vip_clients():
    if dpg.does_item_exist("vip_clients_window"):  # Проверяем, существует ли окно "vip_clients_window"
        return
    with dpg.window(label="VIP клиенты", modal=True, width=600, height=400, tag="vip_clients_window"):  # Создаем новое окно "VIP клиенты"
        with dpg.table(header_row=True):  # Создаем таблицу с заголовком
            dpg.add_table_column(label="Имя клиента")  # Добавляем колонку "Имя клиента"
            dpg.add_table_column(label="Вес груза")  # Добавляем колонку "Вес груза"
            for client in filter(lambda c: c.is_vip, company.clients):
                with dpg.table_row():  # Добавляем строку в таблицу для каждого VIP клиента
                    dpg.add_text(client.name)  # Имя клиента
                    dpg.add_text(str(client.cargo_weight))  # Вес груза клиента
        dpg.add_button(label="Закрыть", callback=lambda: dpg.delete_item("vip_clients_window"))  # Добавляем кнопку "Закрыть" для удаления окна

def show_loaded_vehicles():
    # Проверка, существует ли уже окно с загруженными транспортными средствами
    if dpg.does_item_exist("loaded_vehicles_window"):  # Проверка, существует ли уже окно с загруженными транспортными средствами
        print("Окно с загруженными транспортными средствами уже существует.")  # Сообщение, если окно уже существует
        return

    # Проверка, есть ли транспортные средства с загрузкой больше нуля
    loaded_vehicles = list(filter(lambda v: v.current_load > 0, company.vehicles))  # Фильтрация транспортных средств с загрузкой больше нуля
    if not loaded_vehicles:  # Проверка, есть ли загруженные транспортные средства
        print("Нет загруженных транспортных средств.")  # Сообщение, если нет загруженных транспортных средств
        return

    with dpg.window(label="Загруженные транспортные средства", modal=True, width=600, height=400, tag="loaded_vehicles_window"):  # Создание нового окна "Загруженные транспортные средства"
        with dpg.table(header_row=True):  # Создание таблицы с заголовком
            dpg.add_table_column(label="ID")  # Добавление колонки "ID"
            dpg.add_table_column(label="Грузоподъемность")  # Добавление колонки "Грузоподъемность"
            dpg.add_table_column(label="Текущая загрузка")  # Добавление колонки "Текущая загрузка"
            dpg.add_table_column(label="Особенности")  # Добавление колонки "Особенности"

            # Добавляем загруженные транспортные средства в таблицу
            for vehicle in loaded_vehicles:
                with dpg.table_row():  # Добавление строки в таблицу для каждого загруженного транспортного средства
                    dpg.add_text(str(vehicle.vehicle_id))  # ID транспортного средства
                    dpg.add_text(str(vehicle.capacity))  # Грузоподъемность
                    dpg.add_text(str(vehicle.current_load))  # Текущая загрузка

                    # Проверка типа транспортного средства
                    if isinstance(vehicle, Airplane):
                        dpg.add_text(f"Высота: {vehicle.max_altitude}")  # Высота для самолета
                    elif isinstance(vehicle, Van):
                        dpg.add_text(f"Холодильник: {'Да' if vehicle.is_refrigerated else 'Нет'}")  # Холодильник для фургона


        dpg.add_button(label="Закрыть", callback=lambda: dpg.delete_item("loaded_vehicles_window"))

    print("Окно с загруженными транспортными средствами создано.")


def show_client_form():
    if dpg.does_item_exist("client_form"):  # Проверка, существует ли уже форма клиента
        return
    with dpg.window(label="Добавить клиента", width=450, height=350, modal=True, tag="client_form"):  # Создание нового окна "Добавить клиента"
        dpg.add_text("Имя клиента:")  # Добавление текста "Имя клиента:"
        dpg.add_input_text(tag="client_name", width=300)  # Добавление поля ввода для имени клиента
        dpg.add_text("Вес груза:")  # Добавление текста "Вес груза:"
        dpg.add_input_text(tag="client_cargo_weight", width=300)  # Добавление поля ввода для веса груза
        dpg.add_text("VIP статус:")  # Добавление текста "VIP статус:"
        dpg.add_checkbox(tag="client_is_vip")  # Добавление чекбокса для VIP статуса
        dpg.add_button(label="Сохранить", callback=save_client)  # Добавление кнопки "Сохранить" с вызовом функции save_client
        dpg.add_button(label="Отмена", callback=lambda: dpg.delete_item("client_form"))  # Добавление кнопки "Отмена" для удаления формы

def save_client():
    name = dpg.get_value("client_name")  # Получение значения имени клиента
    cargo_weight = dpg.get_value("client_cargo_weight")  # Получение значения веса груза
    is_vip = dpg.get_value("client_is_vip")  # Получение значения VIP статуса

    if name and cargo_weight.isdigit() and int(cargo_weight) > 0:  # Проверка корректности введенных данных
        client = Client(name, int(cargo_weight), is_vip)  # Создание объекта клиента
        company.add_client(client)  # Добавление клиента в компанию
        update_clients_table()  # Обновление таблицы клиентов
        dpg.delete_item("client_form")  # Удаление формы клиента
    else:
        dpg.set_value("status", "Ошибка: Проверьте введённые данные!")  # Установка сообщения об ошибке


def show_vehicle_form():
    if dpg.does_item_exist("vehicle_form"):  # Проверка, существует ли уже форма транспорта
        return
    with dpg.window(label="Добавить транспорт", width=450, height=350, modal=True, tag="vehicle_form"):  # Создание нового окна "Добавить транспорт"
        dpg.add_text("Тип транспорта:")  # Добавление текста "Тип транспорта:"
        dpg.add_combo(["Самолет", "Фургон"], tag="vehicle_type", width=250, callback=toggle_vehicle_specific_fields)  # Добавление выпадающего списка для выбора типа транспорта
        dpg.add_text("Грузоподъемность (тонны):")  # Добавление текста "Грузоподъемность (тонны):"
        dpg.add_input_text(tag="vehicle_capacity", width=250)  # Добавление поля ввода для грузоподъемности

        dpg.add_text("Введите высоту полёта:", tag="max_altitude_label", show=False)  # Добавление текста "Введите высоту полёта:" (скрыто)
        dpg.add_input_text(tag="max_altitude", width=250, show=False)  # Добавление поля ввода для высоты полёта (скрыто)

        dpg.add_text("Есть ли холодильник:", tag="refrigerator_label", show=False)  # Добавление текста "Есть ли холодильник:" (скрыто)
        dpg.add_checkbox(tag="refrigerator", show=False)  # Добавление чекбокса для холодильника (скрыто)

        dpg.add_button(label="Сохранить", callback=save_vehicle)  # Добавление кнопки "Сохранить" с вызовом функции save_vehicle
        dpg.add_button(label="Отмена", callback=lambda: dpg.delete_item("vehicle_form"))  # Добавление кнопки "Отмена" для удаления формы

def toggle_vehicle_specific_fields(sender, app_data):
    if app_data == "Самолет":
        dpg.configure_item("max_altitude_label", show=True)  # Показать поле для высоты полёта
        dpg.configure_item("max_altitude", show=True)  # Показать поле для ввода высоты полёта
        dpg.configure_item("refrigerator_label", show=False)  # Скрыть поле для холодильника
        dpg.configure_item("refrigerator", show=False)  # Скрыть чекбокс для холодильника
    elif app_data == "Фургон":
        dpg.configure_item("max_altitude_label", show=False)  # Скрыть поле для высоты полёта
        dpg.configure_item("max_altitude", show=False)  # Скрыть поле для ввода высоты полёта
        dpg.configure_item("refrigerator_label", show=True)  # Показать поле для холодильника
        dpg.configure_item("refrigerator", show=True)  # Показать чекбокс для холодильника


def save_vehicle():
    vehicle_type = dpg.get_value("vehicle_type")  # Получение типа транспортного средства
    capacity = dpg.get_value("vehicle_capacity")  # Получение грузоподъемности

    if capacity.isdigit() and int(capacity) > 0:  # Проверка корректности введенной грузоподъемности
        capacity = int(capacity)
        if vehicle_type == "Самолет":
            max_altitude = dpg.get_value("max_altitude")  # Получение высоты полёта
            if max_altitude.isdigit() and int(max_altitude) > 0:  # Проверка корректности введенной высоты полёта
                vehicle = Airplane(capacity, int(max_altitude))  # Передаем высоту полёта
            else:
                dpg.set_value("status", "Ошибка: Проверьте высоту полёта!")  # Установка сообщения об ошибке
                return
        elif vehicle_type == "Фургон":
            has_refrigerator = dpg.get_value("refrigerator")  # Получение значения холодильника
            vehicle = Van(capacity, has_refrigerator)  # Создание объекта фургона
        else:
            vehicle = Vehicle(capacity)  # Грузовик по умолчанию

        company.add_vehicle(vehicle)  # Добавление транспортного средства
        update_vehicles_table()  # Обновление таблицы транспортных средств
        dpg.delete_item("vehicle_form")  # Закрытие формы
    else:
        dpg.set_value("status", "Ошибка: Проверьте введённые данные!")  # Установка сообщения об ошибке



def show_authorized_clients():
    
    # Проверка существования окна
    if dpg.does_item_exist("clients_window"):
        return

# Создаем окно с VIP клиентами
    with dpg.window(label="VIP клиенты", modal=True, width=600, height=400, tag="clients_window"):  # Создаем новое окно "VIP клиенты"
        # Добавляем таблицу с данными
        with dpg.table(header_row=True):  # Создаем таблицу с заголовком
            dpg.add_table_column(label="Имя клиента")  # Добавляем колонку "Имя клиента"
            dpg.add_table_column(label="Вес груза")  # Добавляем колонку "Вес груза"
            dpg.add_table_column(label="VIP статус")  # Добавляем колонку "VIP статус"

            for client in filter(lambda c: c.is_vip, company.clients):  # Проходим по всем VIP клиентам
                with dpg.table_row():  # Добавляем строку в таблицу для каждого VIP клиента
                    dpg.add_text(client.name)  # Имя клиента
                    dpg.add_text(str(client.cargo_weight))  # Вес груза клиента
                    dpg.add_text("Да")  # VIP статус клиента
        
        dpg.add_button(label="Закрыть", callback=lambda: dpg.delete_item("clients_window")) # Кнопка для закрытия окна


def export_results():
    data = {
        "clients": [{"name": c.name, "cargo_weight": c.cargo_weight, "is_vip": c.is_vip} for c in company.clients],  # Список клиентов с их данными
        "vehicles": [
            {
                "vehicle_id": v.vehicle_id,  # ID транспортного средства
                "capacity": v.capacity,  # Грузоподъемность транспортного средства
                "current_load": v.current_load,  # Текущая загрузка транспортного средства
                "type": "Airplane" if isinstance(v, Airplane) else "Van" if isinstance(v, Van) else "Truck",  # Тип транспортного средства
                "details": {
                    "max_altitude": getattr(v, 'max_altitude', None),  # Высота полёта для самолета
                    "has_refrigerator": getattr(v, 'has_refrigerator', None)  # Наличие холодильника для фургона
                }
            } for v in company.vehicles  # Проходим по всем транспортным средствам
        ]
    }

    with open("base.json", "w", encoding="utf-8") as file:  # "base.json" для записи
        json.dump(data, file, ensure_ascii=False, indent=4)  # Записываем данные в файл в формате JSON с отступами
    dpg.set_value("status", "Результаты экспортированы в файл base.json.")  # Устанавливаем сообщение о статусе экспорта


def optimize_cargo_distribution():
    company.distribute_cargo()  # Распределяем грузы по транспортным средствам
    update_vehicles_table()  # Обновляем таблицу транспортных средств
    dpg.set_value("status", "Грузы успешно распределены!")  # Устанавливаем сообщение о статусе распределения

def distribute_cargo_results():
    # Проверяем, существует ли уже окно с результатами распределения
    if dpg.does_item_exist("cargo_distribution_window"):  # Проверка, существует ли уже окно с результатами распределения
        return


    # Создаем окно для отображения результатов
    with dpg.window(label="Распределение груза", modal=True, width=800, height=400, tag="cargo_distribution_window"):
        # Создаем таблицу для отображения результатов
        with dpg.table(header_row=True):
            dpg.add_table_column(label="Транспортное средство")
            dpg.add_table_column(label="Грузоподъемность")
            dpg.add_table_column(label="Текущий груз")
            dpg.add_table_column(label="Распределенный груз")

            # Пример распределения груза: для каждого транспортного средства
            for vehicle in company.vehicles:
                # Пример распределения груза
                distributed_cargo = vehicle.current_load
                with dpg.table_row():
                    dpg.add_text(vehicle.vehicle_id)  # Идентификатор транспортного средства
                    dpg.add_text(str(vehicle.capacity))  # Грузоподъемность
                    dpg.add_text(str(vehicle.current_load))  # Текущий груз
                    dpg.add_text(str(distributed_cargo))  # Распределенный груз

        # Кнопка для закрытия окна
        dpg.add_button(label="Закрыть", callback=lambda: dpg.delete_item("cargo_distribution_window"))


def show_about():
    if dpg.does_item_exist("about_window"):  # Проверка, существует ли уже окно "about_window"
        return

    with dpg.window(label="О программе", width=400, height=300, modal=True, tag="about_window"):  # Создание нового окна "О программе"
        dpg.add_text("Лабораторная работа номер 12")  # Добавление текста "Лабораторная работа номер 12"
        dpg.add_text("Вариант: 4")  # Добавление текста "Вариант: 4"
        dpg.add_text("Разработчик: Зуй Никита Юрьевич")  # Добавление текста "Разработчик: Зуй Никита Юрьевич"
        dpg.add_button(label="Закрыть", callback=lambda: dpg.delete_item("about_window"))  # Добавление кнопки "Закрыть" для удаления окна

def setup_fonts():
    with dpg.font_registry():  # Создание реестра шрифтов
        with dpg.font("C:/Windows/Fonts/Arial.ttf", 24) as default_font:  # Добавление шрифта Arial размером 24
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)  # Добавление диапазона шрифтов по умолчанию
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)  # Добавление диапазона шрифтов для кириллицы
            dpg.bind_font(default_font)  # Привязка шрифта по умолчанию


def optimize_cargo_distribution():
    company.optimize_cargo_distribution()  # Вызываем метод для распределения грузов
    update_vehicles_table()  # Обновляем таблицу с транспортными средствами
    dpg.set_value("status", "Грузы успешно распределены!")


def setup_global_key_handlers():
    """
    Настройка глобальных обработчиков клавиш для всех окон.
    """
    def handle_escape():
        # Закрытие всех открытых окон
        open_windows = [
            "client_form",  # Форма клиента
            "vehicle_form",  # Форма транспортного средства
            "clients_window",  # Окно клиентов
            "all_vehicles_window",  # Окно всех транспортных средств
            "about_window",  # Окно "О программе"
            "all_clients_window",  # Окно всех клиентов
            "cargo_distribution_window",  # Окно распределения грузов
            "cargo_distribution_window",  # Окно распределения грузов (повтор)
        ]
        for window in open_windows:
            if dpg.does_item_exist(window):  # Проверка, существует ли окно
                dpg.delete_item(window)  # Удаление окна

    def handle_enter():
        # Сохранение данных в активной форме
        if dpg.does_item_exist("client_form"):  # Проверка, существует ли форма клиента
            save_client()  # Сохранение данных клиента
        elif dpg.does_item_exist("vehicle_form"):  # Проверка, существует ли форма транспортного средства
            save_vehicle()  # Сохранение данных транспортного средства


    # Глобальная регистрация обработчиков
    with dpg.handler_registry():
        # Escape: закрыть окна
        dpg.add_key_down_handler(key=dpg.mvKey_Escape, callback=lambda: handle_escape())
        # Enter: сохранить данные
        dpg.add_key_down_handler(key=dpg.mvKey_Return, callback=lambda: handle_enter())

def main_window():
    with dpg.window(label="Основное окно", width=1920, height=1080):  # Создаем основное окно
        dpg.add_button(label="О программе", callback=show_about)  # Добавляем кнопку "О программе" с вызовом функции show_about

        with dpg.group(horizontal=True):  # Создаем горизонтальную группу
            # Клиенты
            with dpg.group():  # Создаем группу для клиентов
                dpg.add_text("Клиенты", tag="clients_text")  # Добавляем текст "Клиенты"
                with dpg.table(tag="clients_table", header_row=True):  # Создаем таблицу для клиентов
                    dpg  # Пустая строка для таблицы
                dpg.add_button(label="Добавить клиента", callback=show_client_form)  # Добавляем кнопку "Добавить клиента" с вызовом функции show_client_form
                dpg.add_button(label="Показать всех клиентов", callback=show_all_clients)  # Добавляем кнопку "Показать всех клиентов" с вызовом функции show_all_clients
                dpg.add_button(label="Показать VIP клиентов", callback=show_authorized_clients)  # Добавляем кнопку "Показать VIP клиентов" с вызовом функции show_authorized_clients

            # Транспортные средства
            with dpg.group():  # Создаем группу для транспортных средств
                dpg.add_text("Транспортные средства", tag="vehicles_text")  # Добавляем текст "Транспортные средства"
                with dpg.table(tag="vehicles_table", header_row=True):  # Создаем таблицу для транспортных средств
                    dpg  # Пустая строка для таблицы
                dpg.add_button(label="Добавить транспорт", callback=show_vehicle_form)  # Добавляем кнопку "Добавить транспорт" с вызовом функции show_vehicle_form
                dpg.add_button(label="Распределить грузы", callback=optimize_cargo_distribution)  # Добавляем кнопку "Распределить грузы" с вызовом функции optimize_cargo_distribution
                dpg.add_button(label="Показать все транспортные средства", callback=show_all_vehicles)  # Добавляем кнопку "Показать все транспортные средства" с вызовом функции show_all_vehicles
                dpg.add_button(label="Показать результат распределения", callback=distribute_cargo_results)  # Добавляем кнопку "Показать результат распределения" с вызовом функции distribute_cargo_results
                dpg.add_button(label="Экспортировать результат", callback=export_results)  # Добавляем кнопку "Экспортировать результат" с вызовом функции export_results

        dpg.add_text("", tag="status") # Добавляем текстовый элемент с тегом "status"

# Запуск приложения
dpg.create_context()
setup_fonts()
main_window()

# Настройка обработчиков клавиш
setup_global_key_handlers()

dpg.create_viewport(title="Transport company", width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
