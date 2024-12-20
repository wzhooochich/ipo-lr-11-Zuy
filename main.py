from transport import Client, Vehicle, TransportCompany, Van, Airplane

def validate_input(prompt, type_):
    while True:
        try:
            value = input(prompt)
            if type_ == "int":
                value = int(value)
            elif type_ == "float":
                 value = float(value)
            if type(value) == str and not value.strip():
                 raise ValueError("Значение не может быть пустым.")
            return value
        except ValueError:
            print("Ошибка: Введите корректное значение.")
        except Exception:
           print("Ошибка: Введите корректное значение.")

def display_menu():
    print("\n" + " Меню ".center(70, "=") )
    print("""
        1 - Создать клиента
        2 - Добавить транспорт
        3 - Вывести список клиентов
        4 - Вывести информацию о всех транспортах
        5 - Оптимизировать распределение груза
        6 - Вывести распределение груза 
        7 - Выход с программы
    """)
    print("".center(70, "=") )

def create_company():
    name = validate_input("Введите название транспортной компании: ", "str")
    return TransportCompany(name)

def create_client(company):
    name = validate_input("Введите имя клиента: ", "str")
    cargo_weight = validate_input("Введите вес груза клиента: ", "float")
    while True:
       vip = validate_input("Введите, имеет ли клиент VIP (1 - да, 2 - нет): ", "int")
       if vip == 1:
          is_vip = True
          break
       elif vip == 2:
          is_vip = False
          break
       else:
          print("Ошибка: Введите 1 для VIP, 2 для обычного.")
    try:
       client = Client(name, cargo_weight, is_vip)
       company.add_client(client)
       print(f"Клиент {name} успешно создан.")
    except ValueError as e:
        print(f"Ошибка создания клиента: {e}")


def create_transport(company):
    while True:
        type_veh = validate_input("\nВыберите транспорт для добавления (1 - самолет, 2 - фургон): ", "int")
        if type_veh == 1:
           try:
               capacity = validate_input("Введите грузоподъёмность самолёта: ", "float")
               max_altitude = validate_input("Введите максимальную высоту полета: ", "float")
               airplane = Airplane(capacity, max_altitude)
               company.add_vehicle(airplane)
               print(f"Самолёт успешно создан.")
               break
           except ValueError as e:
               print(f"Ошибка создания самолета: {e}")
        elif type_veh == 2:
           try:
               capacity = validate_input("Введите грузоподъёмность фургона: ", "float")
               while True:
                   is_refrigerated = validate_input("Введите, имеет ли фургон холодильник (1 - да, 2 - нет): ", "int")
                   if is_refrigerated == 1:
                        is_refrigerated_bool = True
                        break
                   elif is_refrigerated == 2:
                        is_refrigerated_bool = False
                        break
                   else:
                        print("Ошибка: Введите 1 если есть холодильник, 2 если нет.")
               van = Van(capacity, is_refrigerated_bool)
               company.add_vehicle(van)
               print(f"Фургон успешно создан.")
               break
           except ValueError as e:
               print(f"Ошибка создания фургона: {e}")
        else:
          print("Ошибка: Выберите 1 для самолета, 2 для фургона.")

def display_all_transport(company):
    print("\nВсе транспортные средства: ".center(70, "="))
    if company.vehicles:
       for idx, vehicle in enumerate(company.vehicles, start=1):
          print(f"{idx}) {vehicle}")
    else:
        print("Нет доступных транспортных средств.")
    print()

def display_all_clients(company):
    print("\nВсе клиенты: ".center(70, "="))
    if company.clients:
        for idx, client in enumerate(company.clients, start=1):
            print(f"{idx}. {client}")
    else:
        print("Нет доступных клиентов.")
    print()


def main():
    company = create_company()
    action_count = 0
    while True:
        display_menu()
        choice = validate_input("Выберите пункт меню: ", "int")
        try:
            if choice == 1:
                 create_client(company)
                 action_count += 1
            elif choice == 2:
                create_transport(company)
                action_count += 1
            elif choice == 3:
                 display_all_clients(company)
                 action_count += 1
            elif choice == 4:
                  display_all_transport(company)
                  action_count += 1
            elif choice == 5:
                company.optimize_cargo_distribution()
                action_count += 1
            elif choice == 6:
                  company.display_cargo()
            elif choice == 7:
                 print(f"Выход из программы. Количество операций: {action_count}.")
                 break
            else:
                print("Ошибка: Неверный выбор пункта меню.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")



if __name__ == "__main__":
    main()
