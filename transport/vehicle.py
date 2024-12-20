import random
from abc import ABC, abstractmethod
from .client import Client


class Vehicle(ABC):
    def __init__(self, capacity):
        if not isinstance(capacity, (int, float)) or capacity <= 0:
            raise ValueError("Грузоподъемность должна быть положительным числом.")

        self.vehicle_id = str(random.randint(1000, 9999))
        self.capacity = capacity
        self.current_load = 0
        self.clients_list = []

    @abstractmethod
    def get_type(self):
        """Возвращает тип транспорта."""
        pass

    def load_cargo(self, client):
         if not isinstance(client, Client):
             raise ValueError("client должен быть объектом класса Client")
         if (self.current_load + client.cargo_weight) > self.capacity:
             raise ValueError(f"Превышение грузоподъемности транспортного средства {self.vehicle_id}. Максимальная загрузка {self.capacity}, текущая загрузка {self.current_load}, груз клиента {client.cargo_weight}.")

         self.current_load += client.cargo_weight
         self.clients_list.append(client)


    def __str__(self):
        return f"ID: {self.vehicle_id}, Тип: {self.get_type()}, Грузоподъемность: {self.capacity} тонн, Текущая загрузка: {self.current_load} тонн"