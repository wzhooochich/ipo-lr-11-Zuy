from .vehicle import Vehicle
from .client import Client

class TransportCompany:
    def __init__(self, name):
        if not isinstance(name, str) or not name:
            raise ValueError("Название компании должно быть непустой строкой.")

        self.name = name
        self.vehicles = []
        self.clients = []

    def add_vehicle(self, vehicle):
        if not isinstance(vehicle, Vehicle):
            raise ValueError("Транспортное средство должно быть объектом класса Vehicle.")
        self.vehicles.append(vehicle)

    def list_vehicles(self):
        return [str(vehicle) for vehicle in self.vehicles]

    def add_client(self, client):
        if not isinstance(client, Client):
            raise ValueError("Клиент должен быть объектом класса Client.")
        self.clients.append(client)

    def optimize_cargo_distribution(self):
       # Сортируем клиентов: VIP в начало списка
       sorted_clients = sorted(self.clients, key=lambda client: client.is_vip, reverse=True)
       # Сортируем транспортные средства по грузоподъемности (по убыванию)
       sorted_vehicles = sorted(self.vehicles, key=lambda v: v.capacity, reverse=True)

       for client in sorted_clients:
           for vehicle in sorted_vehicles:
              try:
                  vehicle.load_cargo(client)
                  print(f"Груз клиента {client.name} (вес: {client.cargo_weight}) распределен на транспортное средство {vehicle.vehicle_id}")
                  break # выходим из внутреннего цикла, когда груз распределён
              except ValueError as e:
                   print(f"Не удалось разместить груз клиента {client.name} из-за: {e}")
                   continue # продолжаем перебор транспорта

    def display_cargo(self):
        print("\nРезультат распределения груза:")
        for vehicle in self.vehicles:
            print(vehicle)
            for client in vehicle.clients_list:
                print(f" - {client.name}: {client.cargo_weight} тонн, VIP: {'да' if client.is_vip else 'нет'}")