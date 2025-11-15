```plaintext
Django 
	framework -> own way to work

	create environment 

		$ python3 -m venv myenv
		$ myenv/bin/activate.bat => windows
		$ source myenv/bin/activate => linux/mac

	-> install package (django)
        $ python3 -m pip install --upgrade pip
		$ python3 -m pip install Django

	create django project
        $ mkdir djangotutorial
		$ django-admin startproject mysite djangotutorial
		$ cd djangotutorial
		
        $ python3 manage.py migrate
        $ python3 manage.py runserver

        $ python3 manage.py createsuperuser

	$ mkdir tutorial
	$ django-admin startproject myapp tutorial
```

---

## Understanding Architecture
MTV pattern

```plaintext
user req -> router (urls.py) -> view (views.py) <-> models.py <-> database
									↓
								Template (Html)
									↓
								Response									
```



## Create app - student

$ python3 manage.py startapp student_info
