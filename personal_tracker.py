class Transaction:
    def __init__(self, amount, date, category):
        self.__amount = amount
        self.date = date
        self.category = category

    def get_amount(self):
        return self.__amount

    def set_amount(self, amount):
        return self.__amount += amount


class Polymorphism:

