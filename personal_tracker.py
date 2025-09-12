import datetime

class Transaction:
    """This class represents a single financial event, which encapsulates all the key data points"""
    def __init__(self, amount, date=None, category, description, type):
        self.__amount = amount
        self.date = date if date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.category = category

    def get_amount(self):
        # pass

   def set_amount(self, amount):
       # pass

    def get_details():
        return f"Date is {self.date}, Category is {self.category}, Description is {self.description}"

    def __str__(self):
        return self.get_details()

class Budget:
    """This class encapsulates the overall budget logic"""
    def __init__(self):
        self.transactions = []
        self.income = 0
        self.expenses = 0

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        
        if transaction.amount > 0:
            self.income += transaction.amount
        else:
            self.expenses += abs(transaction.amount)


