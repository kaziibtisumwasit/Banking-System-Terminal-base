import random
import datetime
from abc import ABC


class User(ABC):
    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address


class Bank:
    def __init__(self):
        self.user_account_list = []
        self._bank_balance = 0
        self.loan_balance = 0
        self.loan_option = False

    def add_account(self, account):
        self.user_account_list.append(account)
        print(f"Account added successfully with account number: {
              account.get_account_number()} \nUser Name: {account.name}")

    def find_account(self, user_name):
        for account in self.user_account_list:
            if account.name == user_name:
                return account
        return None

    def user_list(self):
        print("User List:")
        for account in self.user_account_list:
            print(account.name)

    def add_bank_balance(self, balance):
        self._bank_balance += balance

    def decrease_bank_balance(self, balance):
        self._bank_balance -= balance

    def get_bank_balance(self):
        return self._bank_balance

    def add_loan_balance(self, balance):
        if self._bank_balance < balance and balance > 0:
            print("Insufficient balance for loan")
            return
        self.loan_balance += balance

    def total_loan(self):
        print(f"Total Bank Loan Amount: {self.loan_balance}")

    def delete_user(self, username):
        user = self.find_account(username)
        if user:
            self.user_account_list.remove(user)
            print(f"User {username} deleted successfully")
        else:
            print(f"User {username} not found")

    def loan_option_on(self):
        self.loan_option = True

    def loan_option_off(self):
        self.loan_option = False


class Account(User):
    def __init__(self, name, email, address, account_type, bank):
        super().__init__(name, email, address)
        self.account_type = account_type
        self._balance = 0
        self.account_history = []
        self._account_number = self.generate_account_number()
        self.take_loan_count = 0
        self.bank = bank

    def generate_account_number(self):
        return random.randint(101100, 1019999)

    def get_account_number(self):
        return self._account_number

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            now = datetime.datetime.now()
            done = f"Deposited: Done ✅\nDate & Time: {
                now}\nDeposited Amount: {amount}"
            self.account_history.append(done)
            print(done)
            self.bank.add_bank_balance(amount)
            self.check_balance()
        else:
            print("Failed! You entered an invalid amount! ❌")

    def withdraw(self, amount):
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            now = datetime.datetime.now()
            done = f"Withdrawn: Done ✅\nDate & Time: {
                now}\nWithdrawn Amount: {amount}"
            self.account_history.append(done)
            print(done)
            self.bank.decrease_bank_balance(amount)
            self.check_balance()
        else:
            print("Failed! Withdrawal amount exceeded ❌")

    def check_balance(self):
        print(f"Your current balance is: {self._balance}")

    def check_transaction_history(self):
        print("Transaction History:")
        for transaction in self.account_history:
            print(transaction)

    def take_loan(self, amount):
        if self.take_loan_count < 2 and self.bank.loan_option:
            self.take_loan_count += 1
            self._balance += amount
            self.bank.decrease_bank_balance(amount)
            now = datetime.datetime.now()
            done = f"Loan Approved ✅\nDate & Time: {
                now}\nLoan Amount: {amount}"
            self.account_history.append(done)
            self.bank.add_loan_balance(amount)
            self.check_balance()
        else:
            print("Loan limit exceeded or loan option is off")

    def transfer_money(self, user_name, amount):
        if amount > 0 and amount <= self._balance:
            account = self.bank.find_account(user_name)
            if account:
                self._balance -= amount
                account._balance += amount
                now = datetime.datetime.now()
                print(f"Balance transfer successful! ✅\nSender: {
                      self.name} | Receiver: {user_name} | Transfer Amount: {amount}")
                done = f"Balance Transfer Successful! To {
                    user_name}\nDate & Time: {now}\nTransfer Amount: {amount}"
                self.account_history.append(done)
                self.check_balance()
            else:
                print("Account not found! ❌")
        else:
            print("Failed! Transfer amount exceeded ❌")


class Admin(User):
    def __init__(self, name, email, address, bank):
        super().__init__(name, email, address)
        self.bank = bank

    def delete_user(self, username):
        self.bank.delete_user(username)

    def user_list(self):
        self.bank.user_list()

    def total_available_balance(self):
        print(f"Total Available Balance: {self.bank.get_bank_balance()}")

    def total_loan(self):
        self.bank.total_loan()

    def off_loan(self):
        self.bank.loan_option_off()

    def on_loan_option(self):
        self.bank.loan_option_on()


def admin_fun():
    while True:
        print("Welcome to Admin Menu:")
        print("1. Create Admin")
        print("2. Delete User")
        print("3. User List")
        print("4. Total Available Balance")
        print("5. Total Bank Loan Amount")
        print("6. Turn off Loan Option")
        print("7. Turn on Loan Option")
        print("8. Exit")
        try:
            option = int(input("Enter option: "))
        except ValueError:
            print("Press Valid option!")
            continue
        if option == 1:
            name = input("Enter User Name: ")
            email = input("Enter User Email: ")
            address = input("Enter User Address: ")
            admin = Admin(name, email, address, bank)
        elif option == 2:
            username = input("Enter User Name: ")
            admin.delete_user(username)
        elif option == 3:

            admin.user_list()

        elif option == 4:
            admin.total_available_balance()
        elif option == 5:
            admin.total_loan()
        elif option == 6:
            admin.off_loan()
            print("Turned off loan option successfully")
        elif option == 7:
            admin.on_loan_option()
            print("Turned on loan option successfully")
        elif option == 8:
            print("Thank you admin for using ABC Banking System")
            break


def user_fun():
    while True:
        print("\nWelcome to User Menu:")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Check Transaction History")
        print("6. Take Loan")
        print("7. Transfer Money")
        print("8. Exit")
        try:
            option = int(input("Enter option: "))
        except ValueError:
            print("Press Valid option!")
            continue
        if option == 1:
            name = input("Enter User Name: ")
            email = input("Enter User Email: ")
            address = input("Enter User Address: ")
            account_type = input("Enter Account Type (Saving/Current): ")
            user = Account(name, email, address, account_type, bank)
            bank.add_account(user)
        elif option == 2:
            username = input("Enter User Name: ")
            try:
                amount = float(input("Enter Deposit Amount: "))
            except ValueError:
                print("Enter Valid Amount!")
                continue
            user = bank.find_account(username)
            if user:
                user.deposit(amount)
            else:
                print("User not found!")
        elif option == 3:
            username = input("Enter User Name: ")
            try:
                amount = float(input("Enter Withdrawal Amount: "))
            except ValueError:
                print("Enter Valid Amount")
                continue
            user = bank.find_account(username)
            if user:
                user.withdraw(amount)
            else:
                print("User not found!")
        elif option == 4:
            username = input("Enter User Name: ")
            user = bank.find_account(username)
            if user:
                user.check_balance()
            else:
                print("User not found!")
        elif option == 5:
            username = input("Enter User Name: ")
            user = bank.find_account(username)
            if user:
                user.check_transaction_history()
            else:
                print("User not found!")
        elif option == 6:
            username = input("Enter User Name: ")
            try:
                amount = float(input("Enter Loan Amount: "))
            except ValueError:
                print("Enter Valid Amount!")
                continue
            user = bank.find_account(username)
            if user:
                user.take_loan(amount)
            else:
                print("User not found!")
        elif option == 7:
            username_sender = input("Enter Sender User Name: ")
            username_receiver = input("Enter Receiver User Name: ")
            try:
                amount = float(input("Enter Transfer Amount: "))
            except ValueError:
                print("Enter Valid Amount!")
                continue
            user_sender = bank.find_account(username_sender)
            if user_sender:
                user_sender.transfer_money(username_receiver, amount)
            else:
                print("User not found!")
        elif option == 8:
            print("Thank You!")
            break


bank = Bank()

while True:
    print("Press 1 For admin interface")
    print("Press 2 For user interface")
    print("Press 3 For Exit")
    try:
        option_function = int(input('Enter A Option Here :'))
    except ValueError:
        print("Press Valid option!")
        continue
    if option_function == 1:
        admin_fun()
    elif option_function == 2:
        user_fun()
    elif option_function == 3:
        print("Thank you for using Banking System!")
        break
    else:
        print("Incorrect option! Please try again.")
