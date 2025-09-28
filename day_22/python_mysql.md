# Python + Mysql
```bash
python3 -m venv my_env 
source my_env/bin/activate # => linux
my_env/bin/activate.bat # => windows
pip3 install mysql-connector-python
```

## Database commands
```mysql
create database myappdb;
use myappdb;
create table person(
   id int  primary key auto_increment,
   age int,
   name varchar(20)
);
drop table person;
```

## Python code
```py
import mysql.connector
# Database connection details (replace with yours)
db_config = {
   "host": "localhost",
   "user": "root",
   "password": "root",
   "database": "myappdb"
}


def connect_to_database():
   try:
       connection = mysql.connector.connect(**db_config)
       return connection
   except mysql.connector.Error as err:
       print("Error connecting to database:", err)
       return None


connection = connect_to_database()


# Prepare SQL query with placeholders for data
sql = "INSERT INTO person (name, age) VALUES (%s, %s)"
data = ("demo", "25")  # Replace with your data


cursor = connection.cursor()
cursor.execute(sql, data)
connection.commit()  # Commit changes to the database


connection.close()  # Close the connection


connection = connect_to_database()


sql = "SELECT * FROM person"  # Select all columns


cursor = connection.cursor()
cursor.execute(sql)


# Fetch results as a list of tuples
results = cursor.fetchall()


for row in results:
   print(row)  # Print each row of data


connection.close()
```
## Run and Test
```bash
python3 app.py
deactivate
```

## Advanced Topics for Future Learning:
- **Error Handling**: Implement proper error handling mechanisms using try-except blocks to catch exceptions and provide informative error messages.

- **Parameterization**: Leverage prepared statements with parameterization to enhance security and prevent SQL injection attacks.


- **Object Relational Mappers (ORMs)**: Explore ORMs like SQLAlchemy for a more object-oriented approach to database interactions. ORMs simplify data mapping between Python objects and database tables.


- **Connection Pooling**: For high-performance applications, consider connection pooling to manage database connections efficiently. Connection pools reuse existing connections instead of creating new ones for each request, reducing overhead.


- **Transactions**: Understand database transactions for complex operations that involve multiple queries. Transactions ensure data consistency by either committing all changes or rolling them back if any error occurs.


- **Data Validation**: Implement data validation on both the client-side (using JavaScript) and server-side (using Python) to ensure data integrity and prevent invalid data from entering the database.


