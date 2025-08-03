"""

Application shall be a console application
Application must be menu driven
Application will comprise of two menus
    Introduction menu for guest user
        Open Account
        Login
    Menu for logged in user
        Show balance
        Debit
        Credit
        Exit 
Menu must show iteratively after every operation

--------

Application shall be a console application
Application must be menu driven
Menu must show iteratively after every operation
class Customer -> name, pass, bal, credit(), debit(), checkBal()

users = []
count = 1
Press 1 for open account
    cus = Customer(count)
    count=count+1
    
    users -> cus
Press 2 for login
    account
    account + pass
    email + pass
    found_user <- users
    if found
Press 3 for exit
 -3, five, 8 -> repeat
"""
class Bank:
    def __init__(self):
        # self.customers = [] # list.append, index
        self.customers = {} # username -> key
        
    def register(self):
        print("\n----- Registration -----")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        
        if username in self.customers:
            print("This user already has an account")
        else: 
            acc = Account()
            cus = Customer(username, password, acc)
            self.customers[username] = cus
            
    def login(self, username, password):
        print("\n----- Login -----")
        if username in self.customers and self.customers[username].password==password:
            print("Valid user") 
            return self.customers[username]
        else: 
            print("This user does not have any account")
            return
        

class Account:
    def __init__(self):
        self.balance = 5000
    def bebit(self, amount):
        print("\n----- Debit Amount -----")
        self.balance = self.balance - amount
        return amount
    def checkBal(self):
        print("\n----- Check Balance -----")
        return self.balance
    
class Customer:
    def __init__(self, username, password, account):
        self.username = username
        self.password = password
        self.account = account

def main():
    bank = Bank()
    while True:
        print("\n======bank menu=======")
        print("1. Registration")
        print("2. Login")
        print("3. Exit")
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                bank.register()                
                print(bank.customers)
            elif choice == 2:
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                cus = bank.login(username, password)
                
                print(cus.account.checkBal())
            elif choice == 3:
                print("Thanks to visit, ByeBye")
                return
            else:
                pass
        except ValueError:
            print("Please try again with a number")


# Entry point -> first function
if __name__ == "__main__":
    main()