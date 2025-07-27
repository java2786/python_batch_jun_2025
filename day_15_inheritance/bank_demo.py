class Bank:
    def __init__(self, name):
        self.name = name
        
    def display(self):
        print(f"Welcome to {self.name} bank")
        
    def openAccount(self, name):
        print(f"{name} wants to open a savings account in {self.name} bank")
        
class SbiBank(Bank):
    def __init__(self, name, branch):
        self.branch = branch
        super().__init__(name)
        self.ifsc = "sbi776655"
        
    def display(self):
        super().display()
        print(f"Branch: {self.branch}")
        
sbi = SbiBank("SBI", "Ghaziabad")
sbi.display()

sbi.openAccount("Ramesh")