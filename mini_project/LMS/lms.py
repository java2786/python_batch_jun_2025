""" 
Create console based app
Iterative menu
Guest user:
- Open account / Registration
- Login
- Exit
Logged-in User:
- View all avaialble books
- Borrow a book if available
- Return a borrowed book
- Check fine, balance
- Logout

Data -> save in file
-> users.txt
-> books.txt
"""

import os 

USERS_FILE = "users.txt"
BOOKS_FILE = "books.txt"

# load books
def load_books():
    print(not os.path.exists(BOOKS_FILE))
    if(not os.path.exists(BOOKS_FILE)):
        return []
    else:
        # with open(BOOKS_FILE, 'r') as file:
        with open(BOOKS_FILE, 'r') as file:
            # lines = file.readlines()
            # return lines
            return [line.strip() for line in file if line.strip()]

# registration function
def user_registration():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    
    with open(USERS_FILE, 'a') as file:
        file.write(f"{name},{email},{password},0\n")
    print("****** Account created successfully! ******")
    
# login function
def user_login():
    input_email = input("Enter your email: ")
    input_password = input("Enter your password: ")
    
    with open(USERS_FILE, 'r') as file:
        found_user = None
        for line in file:
            name, email, password, balance = line.strip().split(",")
            # print(f"Name: {name}, Email: {email}, Balance: {balance}")
            # if user is valid or not
            if email == input_email and password == input_password:
                print(f"{input_email} is a Valid user")
                found_user = (name, email, balance)
        return found_user

# Main menu
def main_menu():
    while True:
        print("****** Welcome To My Library ******")
        print("1. Open Account")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            user_registration()
        elif choice == "2":
            user = user_login()
            print(f"After login: {user}")
        elif choice == "3":
            print("Thank you for visiting.")
            break
        else:
            print("Invalid choice")

# books = load_books()
# print(books)

# user_registration()
# user_login()

main_menu()