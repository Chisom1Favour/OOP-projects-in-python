import datetime
import os
import json

# Budget data will be stored in this file
class Transaction:
    """This base class is for all financial transactions. It shows encapsulation by bundling data (amount, date, category) with the methods that work on it"""
    def __init__(self, amount, date=None, category):
        self.amount = (float)amount
        self.date = date if date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.category = category
        self.type = "base" # A default type to be overriden by subclasses

    def to_dict(self):
        """Converts the Transaction object to a dictionary for JSON serialization"""
        return {
                "type": self.type,
                "category": self.category,
                "date": self.date,
                "amount": self.amount
                }
    def __str__(self):
        """Returns the string representation of the objects"""
        return f"Date: {self.date} | Category: {self.category} | Amount: ${self.amount:.2f}"

class Income(Transaction):
    """A class for tracking incokme transactions. This demonstrates inheritance"""
    def __init__(self, amount, category, date=None):
        super().__init__(amount, category, date)
        self.type = "income"

    def __str__(self):
        return f"[INCOME] " + super().__str__()


class Expense(Transaction):
    """This class tracks expense transactions. It also inherits from the Transaction base class"""
    def __init__(self, amount, category, date=None):
        super().__init__(amount, category, date)
        self.type = "expense"

    def __str__(self):
        return f"[EXPENSE] " + super().__str__()

class Budget:
    """Manages all transactions and handles data persistence. Thic class encapsulates all the logic for adding, retrieving and saving transactions"""
    def __init__(self, file_path):
        self.file_path = file_path
        self.transactions = []
        self._load_transactions()

    def _load_transactions(self):
        """Loads transactions from the JSON file."""
        if not os.path.exists(self.file_path):
            print("Budget file not found. Starting with an empty budget.")
            return 
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                for d in data:
                    if d['type'] = 'income':
                        self.transaction.append(Income(d['amount'], d['category'], d['date']))
                    elif d['type'] = 'expense':
                        self.transaction.append(Expense(d['amount'], d['category'], d['date']))
        except (IOError, JSONDecodeError) as e:
            print(f"Error loading budget file: {e}. Starting with an empty budget.")
            self.transactions = []

    def save_transactions(self):
        """Saves all transactions to the JSON fuile."""
        data_to_save = [t.to_dict() for t in self.transactions]
        with open(self.file_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)
        print("Budget data saved successfully.")

    def add_transaction(self, transaction):
        """Adds a new transaction object and saves the budget."""
        self.transactions.append(transaction)
        self.save_transactions()
        print("\nTransaction added.")

    def get_balance(self):
        """Calculates and returns the current balance"""
        balance = 0.0
        # This loop is another 
