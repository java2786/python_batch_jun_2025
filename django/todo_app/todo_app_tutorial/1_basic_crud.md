# Django Todo App - Stage 1: Basic CRUD Operations  
  
**Prerequisites:** Python installed, Basic understanding of web applications  
  
---  
  
## What You'll Build  
  
A simple Todo application where you can:  
- **Create** new todos  
- **Read** all todos in a list  
- **Update** existing todos  
- **Delete** todos  
  
Think of it like a digital notebook where Suresh can write down his daily tasks like "Buy groceries", "Call Ramesh", or "Submit assignment".  
  
---  
  
## Part 1: Project Setup   
  
### Step 1: Create Project Directory  
  
Open your terminal/command prompt and run:  
  
```bash  
mkdir django_todo_app  
cd django_todo_app  
```  
  
### Step 2: Create Virtual Environment  
  
```bash  
python -m venv venv  
```  
  
**Activate it:**  
- Windows: `venv\Scripts\activate`  
- Mac/Linux: `source venv/bin/activate`  
  
You'll see `(venv)` appear in your terminal. This means you're inside the virtual environment.  
  
### Step 3: Install Django  
  
```bash  
pip install django  
```  
  
### Step 4: Create Django Project  
  
```bash  
django-admin startproject todoproject .  
```  
  
**Note the dot (.) at the end** - it creates the project in the current directory.  
  
### Step 5: Create Django App  
  
```bash  
python manage.py startapp todos  
```  
  
Your folder structure should look like:  
```  
django_todo_app/  
├── venv/  
├── todoproject/  
│   ├── __init__.py  
│   ├── settings.py  
│   ├── urls.py  
│   └── wsgi.py  
├── todos/  
│   ├── migrations/  
│   ├── __init__.py  
│   ├── admin.py  
│   ├── apps.py  
│   ├── models.py  
│   ├── tests.py  
│   └── views.py  
└── manage.py  
```  
  
### Step 6: Register the App  
  
Open `todoproject/settings.py` and add `'todos'` to `INSTALLED_APPS`:  
  
```python  
INSTALLED_APPS = [  
    'django.contrib.admin',  
    'django.contrib.auth',  
    'django.contrib.contenttypes',  
    'django.contrib.sessions',  
    'django.contrib.messages',  
    'django.contrib.staticfiles',  
    'todos',  # Add this line  
]  
```  
  
---  
  
## Part 2: Create Todo Model   
  
### What is a Model?  
  
A model is like a blueprint for your database table. It defines what information you want to store.  
  
For a todo, we need:  
- Title (what the task is)  
- Description (more details)  
- Completed status (done or not done)  
- Creation date (when was it created)  
  
### Step 7: Define the Model  
  
Open `todos/models.py` and write:  
  
```python  
from django.db import models  
  
class Todo(models.Model):  
    title = models.CharField(max_length=200)  
    description = models.TextField(blank=True)  
    completed = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
      
    def __str__(self):  
        return self.title  
      
    class Meta:  
        ordering = ['-created_at']  
```  
  
**Understanding the Code:**  
- `CharField`: Short text (like "Buy milk")  
- `TextField`: Long text (like detailed instructions)  
- `BooleanField`: True/False (completed or not)  
- `DateTimeField`: Date and time  
- `auto_now_add=True`: Automatically sets date when created  
- `auto_now=True`: Updates date every time you modify  
- `__str__`: Returns title when you print the object  
- `ordering`: Shows newest todos first  
  
### Step 8: Create Database Tables  
  
Run these commands:  
  
```bash  
python manage.py makemigrations  
python manage.py migrate  
```  
  
**What just happened?**  
- `makemigrations`: Django creates instructions to build the database table  
- `migrate`: Django actually creates the table in the database  
  
---  
  
## Part 3: Create Views   
  
Views are like functions that decide what to show on each page.  
  
### Step 9: Create Views  
  
Open `todos/views.py` and replace everything with:  
  
```python  
from django.shortcuts import render, redirect, get_object_or_404  
from .models import Todo  
  
# Show all todos  
def todo_list(request):  
    todos = Todo.objects.all()  
    return render(request, 'todos/todo_list.html', {'todos': todos})  
  
# Create new todo  
def todo_create(request):  
    if request.method == 'POST':  
        title = request.POST.get('title')  
        description = request.POST.get('description')  
          
        Todo.objects.create(  
            title=title,  
            description=description  
        )  
        return redirect('todo_list')  
      
    return render(request, 'todos/todo_form.html')  
  
# Update existing todo  
def todo_update(request, pk):  
    todo = get_object_or_404(Todo, pk=pk)  
      
    if request.method == 'POST':  
        todo.title = request.POST.get('title')  
        todo.description = request.POST.get('description')  
        todo.completed = request.POST.get('completed') == 'on'  
        todo.save()  
        return redirect('todo_list')  
      
    return render(request, 'todos/todo_form.html', {'todo': todo})  
  
# Delete todo  
def todo_delete(request, pk):  
    todo = get_object_or_404(Todo, pk=pk)  
    if request.method == 'POST':  
        todo.delete()  
        return redirect('todo_list')  
    return render(request, 'todos/todo_confirm_delete.html', {'todo': todo})  
  
# Toggle complete status  
def todo_toggle(request, pk):  
    todo = get_object_or_404(Todo, pk=pk)  
    todo.completed = not todo.completed  
    todo.save()  
    return redirect('todo_list')  
```  
  
**Understanding the Views:**  
- `todo_list`: Gets all todos and shows them  
- `todo_create`: Handles creating new todos  
- `todo_update`: Edits existing todos  
- `todo_delete`: Removes todos  
- `todo_toggle`: Quick complete/incomplete toggle  
- `pk`: Primary Key (unique ID of each todo)  
  
---  
  
## Part 4: Setup URLs   
  
### Step 10: Create App URLs  
  
Create a new file `todos/urls.py`:  
  
```python  
from django.urls import path  
from . import views  
  
urlpatterns = [  
    path('', views.todo_list, name='todo_list'),  
    path('create/', views.todo_create, name='todo_create'),  
    path('update/<int:pk>/', views.todo_update, name='todo_update'),  
    path('delete/<int:pk>/', views.todo_delete, name='todo_delete'),  
    path('toggle/<int:pk>/', views.todo_toggle, name='todo_toggle'),  
]  
```  
  
### Step 11: Connect to Project URLs  
  
Open `todoproject/urls.py` and modify it:  
  
```python  
from django.contrib import admin  
from django.urls import path, include  
  
urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('', include('todos.urls')),  
]  
```  
  
---  
  
## Part 5: Create Templates   
  
### Step 12: Create Template Folders  
  
Inside the `todos` folder, create this structure:  
  
```  
todos/  
└── templates/  
    └── todos/  
        ├── base.html  
        ├── todo_list.html  
        ├── todo_form.html  
        └── todo_confirm_delete.html  
```  
  
### Step 13: Create Base Template  
  
Create `todos/templates/todos/base.html`:  
  
```html  
<!DOCTYPE html>  
<html lang="en">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>Todo App</title>  
    <style>  
        * {  
            margin: 0;  
            padding: 0;  
            box-sizing: border-box;  
        }  
        body {  
            font-family: Arial, sans-serif;  
            background-color: #f4f4f4;  
            padding: 20px;  
        }  
        .container {  
            max-width: 800px;  
            margin: 0 auto;  
            background: white;  
            padding: 30px;  
            border-radius: 10px;  
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);  
        }  
        h1 {  
            color: #333;  
            margin-bottom: 20px;  
            text-align: center;  
        }  
        .btn {  
            padding: 10px 20px;  
            background-color: #007bff;  
            color: white;  
            text-decoration: none;  
            border-radius: 5px;  
            border: none;  
            cursor: pointer;  
            display: inline-block;  
        }  
        .btn:hover {  
            background-color: #0056b3;  
        }  
        .btn-danger {  
            background-color: #dc3545;  
        }  
        .btn-danger:hover {  
            background-color: #c82333;  
        }  
        .btn-success {  
            background-color: #28a745;  
        }  
        .btn-success:hover {  
            background-color: #218838;  
        }  
        form {  
            margin-top: 20px;  
        }  
        input[type="text"], textarea {  
            width: 100%;  
            padding: 10px;  
            margin-bottom: 15px;  
            border: 1px solid #ddd;  
            border-radius: 5px;  
        }  
        textarea {  
            height: 100px;  
            resize: vertical;  
        }  
    </style>  
</head>  
<body>  
    <div class="container">  
        {% block content %}  
        {% endblock %}  
    </div>  
</body>  
</html>  
```  
  
### Step 14: Create List Template  
  
Create `todos/templates/todos/todo_list.html`:  
  
```html  
{% extends 'todos/base.html' %}  
  
{% block content %}  
<h1>My Todo List</h1>  
  
<a href="{% url 'todo_create' %}" class="btn">Add New Todo</a>  
  
<div style="margin-top: 30px;">  
    {% if todos %}  
        {% for todo in todos %}  
        <div style="border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; {% if todo.completed %}background-color: #d4edda;{% endif %}">  
            <h3 style="color: {% if todo.completed %}#155724{% else %}#333{% endif %}; margin-bottom: 10px;">  
                {{ todo.title }}  
                {% if todo.completed %}  
                    <span style="color: green; font-size: 14px;">✓ Completed</span>  
                {% endif %}  
            </h3>  
              
            {% if todo.description %}  
            <p style="color: #666; margin-bottom: 10px;">{{ todo.description }}</p>  
            {% endif %}  
              
            <small style="color: #999;">Created: {{ todo.created_at|date:"d M Y, h:i A" }}</small>  
              
            <div style="margin-top: 15px;">  
                <a href="{% url 'todo_toggle' todo.pk %}" class="btn btn-success" style="font-size: 14px;">  
                    {% if todo.completed %}Mark Incomplete{% else %}Mark Complete{% endif %}  
                </a>  
                <a href="{% url 'todo_update' todo.pk %}" class="btn" style="font-size: 14px;">Edit</a>  
                <a href="{% url 'todo_delete' todo.pk %}" class="btn btn-danger" style="font-size: 14px;">Delete</a>  
            </div>  
        </div>  
        {% endfor %}  
    {% else %}  
        <p style="text-align: center; color: #999; margin-top: 50px;">No todos yet. Create your first todo!</p>  
    {% endif %}  
</div>  
{% endblock %}  
```  
  
### Step 15: Create Form Template  
  
Create `todos/templates/todos/todo_form.html`:  
  
```html  
{% extends 'todos/base.html' %}  
  
{% block content %}  
<h1>{% if todo %}Edit Todo{% else %}Create New Todo{% endif %}</h1>  
  
<form method="POST">  
    {% csrf_token %}  
      
    <label for="title">Title:</label>  
    <input type="text" id="title" name="title" value="{{ todo.title }}" required>  
      
    <label for="description">Description:</label>  
    <textarea id="description" name="description">{{ todo.description }}</textarea>  
      
    {% if todo %}  
    <label>  
        <input type="checkbox" name="completed" {% if todo.completed %}checked{% endif %}>  
        Mark as completed  
    </label>  
    <br><br>  
    {% endif %}  
      
    <button type="submit" class="btn">{% if todo %}Update{% else %}Create{% endif %}</button>  
    <a href="{% url 'todo_list' %}" class="btn btn-danger">Cancel</a>  
</form>  
{% endblock %}  
```  
  
### Step 16: Create Delete Confirmation Template  
  
Create `todos/templates/todos/todo_confirm_delete.html`:  
  
```html  
{% extends 'todos/base.html' %}  
  
{% block content %}  
<h1>Delete Todo</h1>  
  
<p style="margin: 30px 0;">Are you sure you want to delete "<strong>{{ todo.title }}</strong>"?</p>  
  
<form method="POST">  
    {% csrf_token %}  
    <button type="submit" class="btn btn-danger">Yes, Delete</button>  
    <a href="{% url 'todo_list' %}" class="btn">Cancel</a>  
</form>  
{% endblock %}  
```  
  
---  
  
## Part 6: Run the Application   
  
### Step 17: Start the Server  
  
```bash  
python manage.py runserver  
```  
  
### Step 18: Open in Browser  
  
Go to: `http://127.0.0.1:8000/`  
  
**You should see your Todo application!**  
  
---  
  
## How to Use Your App  
  
1. **Create a Todo:**  
   - Click "Add New Todo"  
   - Enter title: "Call Mahesh about project"  
   - Enter description: "Discuss the requirements for the new feature"  
   - Click Create  
  
2. **View Todos:**  
   - See all your todos on the home page  
   - Newest todos appear first  
  
3. **Mark Complete:**  
   - Click "Mark Complete" button  
   - Todo background turns green  
   - Click "Mark Incomplete" to undo  
  
4. **Edit a Todo:**  
   - Click "Edit" button  
   - Modify the title or description  
   - Click "Update"  
  
5. **Delete a Todo:**  
   - Click "Delete" button  
   - Confirm deletion  
   - Todo is removed from the list  
  
---  
  
## Real-World Example  
  
**Scenario:** Dinesh is a student in Pune preparing for exams.  
  
**His Todos:**  
1. **Title:** "Study Django Models"    
   **Description:** "Complete Chapter 3 from the textbook and practice examples"    
   **Status:** Not completed  
  
2. **Title:** "Submit assignment to Ramesh Sir"    
   **Description:** "Python programming assignment - due Friday"    
   **Status:** Not completed  
  
3. **Title:** "Buy notebooks from D-Mart"    
   **Description:** "Need 3 notebooks and 2 pens"    
   **Status:** Completed ✓  
  
---  
  
## Practice Assignment  
  
### Task 1: Add Priority Field  
Add a priority field to your Todo model with choices: Low, Medium, High  
  
**Hint:** Look up `models.CharField` with `choices` parameter  
  
### Task 2: Add Search Feature  
Create a search box to filter todos by title  
  
**Hint:** Use `Todo.objects.filter(title__icontains=search_query)`  
  
### Task 3: Add Color Coding  
Make high priority todos appear with a red border  
  
**Hint:** Use conditional styling in the template based on priority  
  
---  
  
## Quick Quiz  
  
**Question 1:** What does CRUD stand for?  
- A) Create, Read, Update, Download  
- B) Create, Read, Update, Delete  
- C) Copy, Read, Upload, Delete  
- D) Create, Remove, Update, Deploy  
  
**Question 2:** Which Django command creates the database tables?  
- A) `python manage.py create`  
- B) `python manage.py migrate`  
- C) `python manage.py build`  
- D) `python manage.py setup`  
  
**Question 3:** What is the purpose of `{% csrf_token %}` in forms?  
- A) To style the form  
- B) To validate the form  
- C) To protect against Cross-Site Request Forgery attacks  
- D) To submit the form  
  
**Question 4:** What does `get_object_or_404` do?  
- A) Deletes the object if not found  
- B) Returns the object or shows a 404 error page if not found  
- C) Creates a new object if not found  
- D) Redirects to homepage if object not found  
  
**Question 5:** In the Todo model, what does `auto_now_add=True` do?  
- A) Updates the date every time the object is saved  
- B) Sets the date only when the object is first created  
- C) Deletes old dates automatically  
- D) Displays the current date  
  
---  
  
## Common Errors and Solutions  
  
### Error 1: "No module named 'todos'"  
**Solution:** Make sure you added `'todos'` to `INSTALLED_APPS` in `settings.py`  
  
### Error 2: "TemplateDoesNotExist"  
**Solution:** Check that your template folder structure is correct:  
```  
todos/templates/todos/your_template.html  
```  
  
### Error 3: "CSRF verification failed"  
**Solution:** Make sure you have `{% csrf_token %}` inside every POST form  
  
### Error 4: Page not loading  
**Solution:**   
- Check if server is running (`python manage.py runserver`)  
- Verify URLs are configured correctly  
- Check for typos in URL names  
  
---  
  
## What You Learned  
  
- ✓ Django project and app structure  
- ✓ Creating models (database blueprints)  
- ✓ Writing views (handling requests)  
- ✓ Setting up URLs (routing)  
- ✓ Creating templates (HTML pages)  
- ✓ Basic CRUD operations  
- ✓ Working with forms  
- ✓ Template inheritance  
  
---  
  
## Next Steps  
  
In **Stage 2**, we'll add:  
- User registration and login  
- Each user will have their own todos  
- Authentication and security  
  
**Great job completing Stage 1!** You've built a fully functional Todo application. Take a break, practice the assignments, and get ready for user authentication in the next stage.  
  
---  
  
## Quiz Answers  
  
1. **B** - Create, Read, Update, Delete  
2. **B** - `python manage.py migrate`  
3. **C** - To protect against Cross-Site Request Forgery attacks  
4. **B** - Returns the object or shows a 404 error page if not found  
5. **B** - Sets the date only when the object is first created  
  
---  
  
  