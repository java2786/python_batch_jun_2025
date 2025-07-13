############## TUPLE

# Method 1 to create tuple
books = ("Superman", "Ironman", "Spiderman", "Hulk")
print(type(books))
print(books)

# Method 2 to create tuple
subjects = "Math", "Hindi", "English", "Physics"
print(type(subjects))
print(subjects)

# Method 3 
items = tuple(["Laptop", "Mobile", "Shirt"])
print(type(items))
print(items)

# accessing tuple
print(items[1])    # mobile
print(items[-1])    # last item - shirt

print(books[1:3])

a, b, c = items 
print(a)
print(b)
print(c)

order = ("Laptop", 120000, "Electronics", "CC", "Delivered")

item, price, category, payment_mode, shipping_status = order

print(f"Item: {item}, Price: {price}, Category: {category}, PaymentMode: {payment_mode}, Shipment: {shipping_status}")


############## SET
# watched movies
movie_list = {"Andaz Apna Apna", "Bahubali", "Bahubali", "The Mask", "Avengers", "The Mask"}
movie_list.add("KFG")
# "Andaz Apna Apna", "Bahubali", "The Mask", "Avengers"
print(movie_list)

# to watch
ott_list = {"Panchayat", "Venom", "Andaz Apna Apna", "Bahubali", "XXX"}

all_movies = movie_list.union(ott_list)

print(all_movies)
watched_movies = movie_list.intersection(ott_list)
print(watched_movies)

# ott_list.update("Bahubali", "Bahubali - Part 1")
ott_list.remove("Bahubali")
ott_list.add("Bahubali - Part 1")
print(ott_list)

########### DICTIONARY
temp = {"delhi": 28, "mumbai": 26, "pune": 25}

print(temp)
print(f"Delhi temprature is {temp['delhi']}")