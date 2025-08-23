class Account:
    def __init__(self, user, balance):
        self.user = user 
        self.__balance = balance     # private
        
    def showBalance(self):
        print(f"{self.user}'s Balance: {self.__balance}")
      
      
acc = Account("Ramesh", 12000)
print("Name:",acc.user)
# print("Balance:",acc.__balance)
acc.showBalance()