# Billing system

## Polymorphism = one name - many form

class UPIPayment:
    def __init__(self, upi_id):
        self.upi_id = upi_id
        
    def pay(self, amount):
        return f"UPI {self.upi_id} paid ₹{amount:.2f}"
    
class CardPayment:
    def __init__(self, card_details):
        self.card_details = card_details
        
    def pay(self, amount):
        return f"Card **** {self.card_details} paid ₹{amount:.2f}"
    

def checkout(payment_mode, amount):
    print(payment_mode.pay(amount))
    

checkout(UPIPayment("demo@1133"), 499.9)
checkout(CardPayment("9876"), 1200)

# Built in

print(len([3,4,5,6]))
print(len("demo"))
print(len(("ramesh", "suresh", "mahesh", "dinesh")))

