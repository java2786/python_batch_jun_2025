# Mysql + Django

## Create a MySql Database
Use MySQL Workbench or the command line to create a database for your Django project.

### Use in databse server not in django app
```bash
create database myappdb;
use myappdb;
```

## Create environment
```bash
$ python3 -m venv my_venv 
$ pip install PyMySQL
```

## Modify __init__.py in Your Django Project
```py
import pymysql
pymysql.install_as_MySQLdb()
```

## Django `settings.py` 
```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': '127.0.0.1',  
        'PORT': '3306',       
    }
}
```

## Create database tables in mysql
```bash
python manage.py makemigrations
python manage.py migrate
```


## Start django app
```bash
python manage.py runserver
```



