'''
Sohan's Restaurant, show menu
    Dosa - 80
    Idli - 35
    ColdDrink - 60

Mohan -> 2 Dosa, 5 Idli, 1 ColdDrink 
find total bill
'''

dosaPrice = 50
idliPrice = 25
coldDrinkPrice = 50

print("Welcome to Sohan's Restaurant")
print("Our menu")
print("1. Dosa - Rs",dosaPrice)
print("2. Idli - Rs",idliPrice)
print("3. ColdDrink - Rs",coldDrinkPrice)



# billAmount = (2*dosaPrice)+(5*idliPrice)+(1*coldDrinkPrice)

# System.out.println("Enter amount")
# Scanner scanner = new Scanner(System.in);
# a = Integer.parseInt(scanner.nextLine())

dosaQuantity = int(input("Dosa Quantity: "))
idliQuantity = int(input("Idli Quantity: "))
coldDrinkQuantity = int(input("ColdDrink Quantity: "))

dosaAmount = dosaPrice * dosaQuantity
idliAmount = idliPrice * idliQuantity
cdAmount = coldDrinkPrice * coldDrinkQuantity

print("\n\n===========Mohan's Bill=============")
print(f"Dosa: {dosaQuantity}x Rs {dosaPrice} = {dosaAmount}")
print(f"Idli: {idliQuantity}x Rs {idliPrice} = {idliAmount}")
print(f"ColdDrink: {coldDrinkQuantity}x Rs {coldDrinkPrice} = {cdAmount}")
print("--------------------------------------------------------------------")
print(f"Total bill: Rs {dosaAmount + idliAmount + cdAmount}")
print("Thank you")