def greet():
    print("Welcome User")
    
greet()

def makeMaggie():
    print("Boil water")
    print("Add maggie noodles")
    print("Add masala")
    print("cook for 5 mins")
    print("Maggie is ready")
    
makeMaggie()

def printTable(n):
    for i in range(1, 11):
        print(f"{n} * {i} = {n*i}")
        
printTable(5)
printTable(3)
printTable(7)


def greetUser(username):
    output = f"Welcome {username}"
    return output


a = greetUser("muKeSh")
print(a) # expected output: Welcome Mukesh