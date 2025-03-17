import datetime

class BankAccount:
    total_accounts = 0  
    account_log = {} 
    def __init__(self, name, initial_balance, account_type="Savings"):
        if not name.strip():
            raise ValueError("Account holder name cannot be empty.")
        if initial_balance < 0:
            raise ValueError("Initial balance must be non-negative.")
        self.name = name
        self.balance = initial_balance
        self.account_type = account_type
        self.transactions = []  
        BankAccount.total_accounts += 1
        self.account_number = f"AC{1000 + BankAccount.total_accounts}"
        BankAccount.account_log[self.account_number] = self 
        print(f"Account created successfully! Account Number: {self.account_number}")
    def deposit(self, amount):
        if not BankAccount.validate_transaction(amount):
            return
        self.balance += amount
        self.transactions.append((datetime.datetime.now(), f"Deposit: ₹{amount}"))
        print(f"₹{amount} deposited successfully. New balance: ₹{self.balance}")
    def withdraw(self, amount):
        if not BankAccount.validate_transaction(amount):
            return
        if self.balance - amount < 0:
            print("Insufficient funds! Withdrawal failed.")
            return
        self.balance -= amount
        self.transactions.append((datetime.datetime.now(), f"Withdrawal: ₹{amount}"))
        print(f"₹{amount} withdrawn successfully. New balance: ₹{self.balance}")
    def transfer(self, target_account, amount):
        if not BankAccount.validate_transaction(amount):
            return
        if self.balance - amount < 0:
            print("Insufficient funds! Transfer failed.")
            return
        if target_account not in BankAccount.account_log:
            print("Invalid target account.")
            return
        self.balance -= amount
        BankAccount.account_log[target_account].balance += amount
        self.transactions.append((datetime.datetime.now(), f"Transfer: ₹{amount} to {target_account}"))
        BankAccount.account_log[target_account].transactions.append((datetime.datetime.now(), f"Received: ₹{amount} from {self.account_number}"))
        print(f"₹{amount} transferred to {target_account} successfully.")
    def check_balance(self):
        print(f"Current Balance: ₹{self.balance}")
    def get_transaction_history(self):
        print("\nTransaction History:")
        for t in self.transactions:
            print(f"{t[0]} - {t[1]}")    
    @classmethod
    def get_total_accounts(cls):
        print(f"Total Accounts: {cls.total_accounts}")
    @staticmethod
    def validate_transaction(amount):
        if amount <= 0:
            print("Amount must be greater than ₹0.")
            return False
        if amount > 50000:
            print("Fraud Alert: Transactions over ₹50,000 are not allowed.")
            return False
        return True
class SavingsAccount(BankAccount):
    interest_rate = 0.05  
    minimum_balance = 1000
    def __init__(self, name, initial_balance):
        if initial_balance < self.minimum_balance:
            raise ValueError(f"Minimum balance for Savings Account is ₹{self.minimum_balance}")
        super().__init__(name, initial_balance, "Savings")
    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        self.transactions.append((datetime.datetime.now(), f"Interest Applied: ₹{interest:.2f}"))
        print(f"₹{interest:.2f} interest added. New balance: ₹{self.balance:.2f}")
class CurrentAccount(BankAccount):
    overdraft_limit = 5000
    def __init__(self, name, initial_balance):
        super().__init__(name, initial_balance, "Current")
    def withdraw(self, amount):
        if not BankAccount.validate_transaction(amount):
            return
        if self.balance - amount < -self.overdraft_limit:
            print("Overdraft limit exceeded! Withdrawal failed.")
            return
        self.balance -= amount
        self.transactions.append((datetime.datetime.now(), f"Withdrawal: ₹{amount}"))
        print(f"₹{amount} withdrawn successfully. New balance: ₹{self.balance}")
def main():
    accounts = {}    
    while True:
        print("\n Welcome to the Bank System")
        print("[1] Open Account  [2] Deposit  [3] Withdraw  [4] Transfer")
        print("[5] Check Balance  [6] Transaction History  [7] Total Accounts  [8] Exit")
        choice = input("Enter your choice: ").strip()
        if not choice:
            print("No input provided. Please enter a valid choice.")
            continue
        if choice == "1":
            name = input("Enter Name: ").strip()
            if not name:
                print(" Name cannot be empty.")
                continue
            acc_type = input("Choose Account Type (Savings/Current): ").strip().capitalize()
            if not acc_type:
                print(" Account type cannot be empty.")
                continue
            balance_input = input("Enter Initial Deposit: ").strip()
            if not balance_input:
                print(" Initial deposit cannot be empty.")
                continue
            try:
                balance = float(balance_input)
                if acc_type == "Savings":
                    acc = SavingsAccount(name, balance)
                else:
                    acc = CurrentAccount(name, balance)
                accounts[acc.account_number] = acc
            except ValueError as e:
                print(f" Error: {e}")
        elif choice == "2":
            acc_no = input("Enter Account Number: ").strip()
            if not acc_no:
                print(" Account number cannot be empty.")
                continue
            if acc_no in accounts:
                amount_input = input("Enter Amount to Deposit: ").strip()
                if not amount_input:
                    print(" Deposit amount cannot be empty.")
                    continue
                try:
                    amount = float(amount_input)
                    accounts[acc_no].deposit(amount)
                except ValueError:
                    print(" Invalid amount entered.")
            else:
                print(" Account not found!")
        elif choice == "3":
            acc_no = input("Enter Account Number: ").strip()
            if not acc_no:
                print(" Account number cannot be empty.")
                continue
            if acc_no in accounts:
                amount_input = input("Enter Amount to Withdraw: ").strip()
                if not amount_input:
                    print(" Withdrawal amount cannot be empty.")
                    continue
                try:
                    amount = float(amount_input)
                    accounts[acc_no].withdraw(amount)
                except ValueError:
                    print(" Invalid amount entered.")
            else:
                print(" Account not found!")
        elif choice == "4":
            from_acc = input("Enter Your Account Number: ").strip()
            if not from_acc:
                print(" Your account number cannot be empty.")
                continue
            to_acc = input("Enter Recipient Account Number: ").strip()
            if not to_acc:
                print(" Recipient account number cannot be empty.")
                continue
            if from_acc in accounts:
                amount_input = input("Enter Amount to Transfer: ").strip()
                if not amount_input:
                    print(" Transfer amount cannot be empty.")
                    continue
                try:
                    amount = float(amount_input)
                    accounts[from_acc].transfer(to_acc, amount)
                except ValueError:
                    print(" Invalid amount entered.")
            else:
                print(" Your Account not found!")
        elif choice == "5":
            acc_no = input("Enter Account Number: ").strip()
            if not acc_no:
                print(" Account number cannot be empty.")
                continue
            if acc_no in accounts:
                accounts[acc_no].check_balance()
            else:
                print(" Account not found!")
        elif choice == "6":
            acc_no = input("Enter Account Number: ").strip()
            if not acc_no:
                print(" Account number cannot be empty.")
                continue
            if acc_no in accounts:
                accounts[acc_no].get_transaction_history()
            else:
                print(" Account not found!")
        elif choice == "7":
            BankAccount.get_total_accounts()
        elif choice == "8":
            print(" Thank you for using the Bank System!")
            break
        else:
            print(" Invalid choice, try again.")
if __name__ == "__main__":
    main()
