

def add(num_1: int, num_2: int) -> int:
    return num_1 + num_2 

def subtract(num_1: int, num_2: int) -> int:
    return num_1 - num_2

def multiply(num_1: int, num_2: int) -> int:
    return num_1 * num_2

def divide(num_1: int, num_2: int) -> float:
    if num_2 == 0:
        raise ValueError("Cannot divide by zero")
    return num_1 / num_2


class BankAccount():
    def __init__(self, starting_Balance = 0):
        self.balance = starting_Balance

    def deposite(self, amount):
        self.balance += amount
        return self.balance

   

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise ValueError("Insufficient funds")



    def interest(self, rate):
        self.balance *= rate
        self.balance = round(self.balance, 2)
        return self.balance
    
    def transaction(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise ValueError("Insufficient balance")


