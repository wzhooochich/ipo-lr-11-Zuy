class Client:
    def __init__(self, name, cargo_weight, is_vip=False):
        if not isinstance(name, str) or not name:
            raise ValueError("Имя клиента должно быть непустой строкой.")
        if not isinstance(cargo_weight, (int, float)) or cargo_weight <= 0:
            raise ValueError("Вес груза должен быть положительным числом.")

        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip

    def __str__(self):
        vip_status = "VIP" if self.is_vip else "обычный"
        return f"Клиент: {self.name}, Вес груза: {self.cargo_weight} тонн, Статус: {vip_status}"