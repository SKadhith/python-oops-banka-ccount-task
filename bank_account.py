class BankAccount:
    total_accounts = 0  

    def __init__(self, name, initial_balance=0):
        if not name.strip():
            raise ValueError("Account holder name cannot be empty.")
        if initial_balance < 0:
            raise ValueError("Initial balance must be non-negative.")
        
        self.name = name
        self.balance = initial_balance
        self.transactions = []  
        BankAccount.total_accounts += 1
        print(f"Account created for {self.name} with balance ₹{self.balance}")

    def deposit(self, amount):
        if amount <= 0:
            print("Invalid deposit amount.")
            return
        self.balance += amount
        self.transactions.append(f"Deposited: ₹{amount}")
        print(f"₹{amount} deposited. New balance: ₹{self.balance}")

    def withdraw(self, amount):
        if amount <= 0 or amount > self.balance:
            print("Invalid or insufficient funds.")
            return
        self.balance -= amount
        self.transactions.append(f"Withdrawn: ₹{amount}")
        print(f"₹{amount} withdrawn. New balance: ₹{self.balance}")

    def check_balance(self):
        print(f"{self.name}'s account balance: ₹{self.balance}")

    def transfer(self, recipient, amount):
        if not isinstance(recipient, BankAccount):
            print("Invalid recipient.")
            return
        if amount <= 0 or amount > self.balance:
            print("Invalid or insufficient funds.")
            return

        self.balance -= amount
        recipient.balance += amount
        self.transactions.append(f"Transferred: ₹{amount} to {recipient.name}")
        recipient.transactions.append(f"Received: ₹{amount} from {self.name}")
        print(f"₹{amount} transferred to {recipient.name}")

acc1 = BankAccount("Adhi", 50000)
acc2 = BankAccount("Aarthi", 30000)
acc1.deposit(25000)
acc1.withdraw(1000)
acc1.check_balance()
acc1.transfer(acc2, 1300)
acc2.check_balance()
acc2.withdraw(1000)
acc2.check_balance()
acc1.check_balance()
