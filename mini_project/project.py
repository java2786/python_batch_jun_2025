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

def main():
    balance = 5000
    while True:
        print("\n======bank menu=======")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. exit")
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                print(f"Your balance is {balance}")
            elif choice == 2:
                amount = int(input("Enter amount to credit: "))
                print(f"{amount} successfully deposited")
                balance = balance + amount
            elif choice == 3:
                amount = int(input("Enter amount to debit: "))
                if amount<=balance:
                    print(f"{amount} successfully debitted")
                    balance = balance - amount
                else:
                    print("You do not have enough balance")
            elif choice == 4:
                print("Bye Bye")
                return
            else:
                print("Invalid choice")
        except ValueError:
            print("Please try again with a number")


# Entry point -> first function
if __name__ == "__main__":
    main()