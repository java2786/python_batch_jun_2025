import gc 

class Person:
    def __init__(self,name):
        self.name = name 
        self.partner = None 

    def __del__(self):
        print(f"{self.name} is done")
        
p1 = Person("Virat")
p2 = Person("Anushka")

p1.partner = p2 
p2.partner = p1 

del p1 
del p2

gc.collect() # forcing gc
print("ByeBye")