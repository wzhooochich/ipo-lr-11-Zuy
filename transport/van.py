from .vehicle import Vehicle

class Van(Vehicle):
    def __init__(self, capacity, is_refrigerated):
        super().__init__(capacity)
        if not isinstance(is_refrigerated, bool):
            raise ValueError("Флаг холодильника должен быть булевым значением.")
        self.is_refrigerated = is_refrigerated

    def get_type(self):
       return "Фургон"

    def __str__(self):
        return f"{super().__str__()} , Холодильник: {'есть' if self.is_refrigerated else 'нет'}"