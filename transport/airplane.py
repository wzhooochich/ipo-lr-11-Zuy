from .vehicle import Vehicle

class Airplane(Vehicle):
    def __init__(self, capacity, max_altitude):
        super().__init__(capacity)
        if not isinstance(max_altitude, (int, float)) or max_altitude <= 0:
            raise ValueError("Максимальная высота полета должна быть положительным числом.")

        self.max_altitude = max_altitude

    def get_type(self):
       return "Самолет"

    def __str__(self):
        return f"{super().__str__()} , Максимальная высота полета: {self.max_altitude} метров"