# Django Todo App - Stage 2: User Authentication  
  
**Prerequisites:** Completed Stage 1 (Basic CRUD)  
  
---  
  
## What You'll Build  
  
In this stage, you'll add:  
- **User Registration** - New users can create accounts  
- **User Login/Logout** - Users can sign in and out  
- **Protected Pages** - Only logged-in users can create/edit todos  
- **User-specific Todos** - Each user sees only their own todos  
  
**Real-World Example:**    
Imagine Suresh and Ramesh both use the same todo app. Right now, they both see all todos. After Stage 2, Suresh will see only his todos, and Ramesh will see only his todos. Perfect for privacy!  
  
---  
  
## Part 1: Update Todo Model   
  
### Why Do We Need This?  
  
Currently, todos don't belong to anyone. We need to connect each todo to a specific user.  
  
### Step 1: Modify the Todo Model  
  
Open `todos/models.py` and update it:  
  
```python  
from django.db import models  
from django.contrib.auth.models import User  
  
class Todo(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')  
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
  
**What Changed?**  
- Added `user = models.ForeignKey(User, on_delete=models.CASCADE)`  
- This connects each todo to a user  
- `on_delete=models.CASCADE` means if user is deleted, their todos are also deleted  
- `related_name='todos'` allows us to access todos like `user.todos.all()`  
  
### Step 2: Handle Existing Todos  
  
Since we changed the model, we need to update the database. But there's a problem - existing todos don't have a user assigned!  
  
**Solution:** We'll delete old data and start fresh.  
  
```bash  
# Delete the database file  
rm db.sqlite3  
  
# Delete all migration files except __init__.py  
rm todos/migrations/0*.py  
  
# Create fresh migrations  
python manage.py makemigrations  
python manage.py migrate  
```  
  
**Note:** In real projects, you'd use data migration. For learning, starting fresh is simpler.  
  
---  
  
## Part 2: Create Authentication Views   
  
### Step 3: Create Authentication Views  
  
Open `todos/views.py` and add these new views at the bottom:  
  
```python  
from django.shortcuts import render, redirect, get_object_or_404  
from django.contrib.auth import login, logout, authenticate  
from django.contrib.auth.decorators import login_required  
from django.contrib.auth.models import User  
from django.contrib import messages  
from .models import Todo  
  
# ========== TODO VIEWS (UPDATE EXISTING) ==========  
  
@login_required  
def todo_list(request):  
    todos = Todo.objects.filter(user=request.user)  
    return render(request, 'todos/todo_list.html', {'todos': todos})  
  
@login_required  
def todo_create(request):  
    if request.method == 'POST':  
        title = request.POST.get('title')  
        description = request.POST.get('description')  
          
        Todo.objects.create(  
            user=request.user,  
            title=title,  
            description=description  
        )  
        messages.success(request, 'Todo created successfully!')  
        return redirect('todo_list')  
      
    return render(request, 'todos/todo_form.html')  
  
@login_required  
def todo_update(request, pk):  
    todo = get_object_or_404(Todo, pk=pk, user=request.user)  
      
    if request.method == 'POST':  
        todo.title = request.POST.get('title')  
        todo.description = request.POST.get('description')  
        todo.completed = request.POST.get('completed') == 'on'  
        todo.save()  
        messages.success(request, 'Todo updated successfully!')  
        return redirect('todo_list')  
      
    return render(request, 'todos/todo_form.html', {'todo': todo})  
  
@login_required  
def todo_delete(request, pk):  
    todo = get_object_or_404(Todo, pk=pk, user=request.user)  
    if request.method == 'POST':  
        todo.delete()  
        messages.success(request, 'Todo deleted successfully!')  
        return redirect('todo_list')  
    return render(request, 'todos/todo_confirm_delete.html', {'todo': todo})  
  
@login_required  
def todo_toggle(request, pk):  
    todo = get_object_or_404(Todo, pk=pk, user=request.user)  
    todo.completed = not todo.completed  
    todo.save()  
    return redirect('todo_list')  
  
  
# ========== AUTHENTICATION VIEWS (NEW) ==========  
  
def register_view(request):  
    if request.user.is_authenticated:  
        return redirect('todo_list')  
      
    if request.method == 'POST':  
        username = request.POST.get('username')  
        email = request.POST.get('email')  
        password = request.POST.get('password')  
        password2 = request.POST.get('password2')  
          
        # Validation  
        if password != password2:  
            messages.error(request, 'Passwords do not match!')  
            return render(request, 'todos/register.html')  
          
        if User.objects.filter(username=username).exists():  
            messages.error(request, 'Username already exists!')  
            return render(request, 'todos/register.html')  
          
        if User.objects.filter(email=email).exists():  
            messages.error(request, 'Email already registered!')  
            return render(request, 'todos/register.html')  
          
        # Create user  
        user = User.objects.create_user(  
            username=username,  
            email=email,  
            password=password  
        )  
          
        messages.success(request, f'Account created for {username}! Please login.')  
        return redirect('login')  
      
    return render(request, 'todos/register.html')  
  
  
def login_view(request):  
    if request.user.is_authenticated:  
        return redirect('todo_list')  
      
    if request.method == 'POST':  
        username = request.POST.get('username')  
        password = request.POST.get('password')  
          
        user = authenticate(request, username=username, password=password)  
          
        if user is not None:  
            login(request, user)  
            messages.success(request, f'Welcome back, {username}!')  
            return redirect('todo_list')  
        else:  
            messages.error(request, 'Invalid username or password!')  
      
    return render(request, 'todos/login.html')  
  
  
@login_required  
def logout_view(request):  
    logout(request)  
    messages.success(request, 'You have been logged out successfully!')  
    return redirect('login')  
```  
  
**Key Changes Explained:**  
  
1. **@login_required decorator:**   
   - Forces users to login before accessing the view  
   - Redirects to login page if not logged in  
  
2. **Filter by user:**  
   - `Todo.objects.filter(user=request.user)` - shows only current user's todos  
   - `get_object_or_404(Todo, pk=pk, user=request.user)` - ensures user can only edit their own todos  
  
3. **Messages:**  
   - `messages.success()` - shows success notifications  
   - `messages.error()` - shows error notifications  
  
---  
  
## Part 3: Update URLs   
  
### Step 4: Add Authentication URLs  
  
Open `todos/urls.py` and update it:  
  
```python  
from django.urls import path  
from . import views  
  
urlpatterns = [  
    # Todo URLs  
    path('', views.todo_list, name='todo_list'),  
    path('create/', views.todo_create, name='todo_create'),  
    path('update/<int:pk>/', views.todo_update, name='todo_update'),  
    path('delete/<int:pk>/', views.todo_delete, name='todo_delete'),  
    path('toggle/<int:pk>/', views.todo_toggle, name='todo_toggle'),  
      
    # Authentication URLs  
    path('register/', views.register_view, name='register'),  
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'),  
]  
```  
  
### Step 5: Configure Login URL  
  
Open `todoproject/settings.py` and add at the bottom:  
  
```python  
# Redirect to login page if user is not authenticated  
LOGIN_URL = 'login'  
LOGIN_REDIRECT_URL = 'todo_list'  
LOGOUT_REDIRECT_URL = 'login'  
```  
  
---  
  
## Part 4: Create Authentication Templates   
  
### Step 6: Update Base Template with Navbar  
  
Replace `todos/templates/todos/base.html`:  
  
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
        }  
        .navbar {  
            background-color: #007bff;  
            color: white;  
            padding: 15px 20px;  
            display: flex;  
            justify-content: space-between;  
            align-items: center;  
        }  
        .navbar h2 {  
            margin: 0;  
        }  
        .navbar a {  
            color: white;  
            text-decoration: none;  
            margin-left: 20px;  
        }  
        .navbar a:hover {  
            text-decoration: underline;  
        }  
        .container {  
            max-width: 800px;  
            margin: 30px auto;  
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
        .messages {  
            list-style: none;  
            margin-bottom: 20px;  
        }  
        .messages li {  
            padding: 10px;  
            margin-bottom: 10px;  
            border-radius: 5px;  
        }  
        .messages .success {  
            background-color: #d4edda;  
            color: #155724;  
            border: 1px solid #c3e6cb;  
        }  
        .messages .error {  
            background-color: #f8d7da;  
            color: #721c24;  
            border: 1px solid #f5c6cb;  
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
        input[type="text"],   
        input[type="email"],   
        input[type="password"],   
        textarea {  
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
        label {  
            display: block;  
            margin-bottom: 5px;  
            color: #333;  
            font-weight: bold;  
        }  
        .form-link {  
            text-align: center;  
            margin-top: 15px;  
        }  
        .form-link a {  
            color: #007bff;  
            text-decoration: none;  
        }  
        .form-link a:hover {  
            text-decoration: underline;  
        }  
    </style>  
</head>  
<body>  
    {% if user.is_authenticated %}  
    <div class="navbar">  
        <h2>Todo App</h2>  
        <div>  
            <span>Welcome, {{ user.username }}!</span>  
            <a href="{% url 'todo_list' %}">My Todos</a>  
            <a href="{% url 'logout' %}">Logout</a>  
        </div>  
    </div>  
    {% endif %}  
  
    <div class="container">  
        {% if messages %}  
        <ul class="messages">  
            {% for message in messages %}  
            <li class="{{ message.tags }}">{{ message }}</li>  
            {% endfor %}  
        </ul>  
        {% endif %}  
  
        {% block content %}  
        {% endblock %}  
    </div>  
</body>  
</html>  
```  
  
### Step 7: Create Registration Template  
  
Create `todos/templates/todos/register.html`:  
  
```html  
{% extends 'todos/base.html' %}  
  
{% block content %}  
<h1>Create Account</h1>  
  
<form method="POST">  
    {% csrf_token %}  
      
    <label for="username">Username:</label>  
    <input type="text" id="username" name="username" required>  
      
    <label for="email">Email:</label>  
    <input type="email" id="email" name="email" required>  
      
    <label for="password">Password:</label>  
    <input type="password" id="password" name="password" required>  
      
    <label for="password2">Confirm Password:</label>  
    <input type="password" id="password2" name="password2" required>  
      
    <button type="submit" class="btn">Register</button>  
</form>  
  
<div class="form-link">  
    <p>Already have an account? <a href="{% url 'login' %}">Login here</a></p>  
</div>  
{% endblock %}  
```  
  
### Step 8: Create Login Template  
  
Create `todos/templates/todos/login.html`:  
  
```html  
{% extends 'todos/base.html' %}  
  
{% block content %}  
<h1>Login</h1>  
  
<form method="POST">  
    {% csrf_token %}  
      
    <label for="username">Username:</label>  
    <input type="text" id="username" name="username" required>  
      
    <label for="password">Password:</label>  
    <input type="password" id="password" name="password" required>  
      
    <button type="submit" class="btn">Login</button>  
</form>  
  
<div class="form-link">  
    <p>Don't have an account? <a href="{% url 'register' %}">Register here</a></p>  
</div>  
{% endblock %}  
```  
  
---  
  
## Part 5: Test the Application   
  
### Step 9: Create Test Users  
  
Start the server:  
```bash  
python manage.py runserver  
```  
  
### Test Scenario 1: Registration  
  
1. Go to `http://127.0.0.1:8000/register/`  
2. Create first user:  
   - Username: `suresh`  
   - Email: `suresh@gmail.com`  
   - Password: `suresh123`  
   - Confirm Password: `suresh123`  
3. Click "Register"  
4. You'll be redirected to login page  
  
### Test Scenario 2: Login  
  
1. Login with:  
   - Username: `suresh`  
   - Password: `suresh123`  
2. You'll see "Welcome back, suresh!" message  
  
### Test Scenario 3: Create Todos  
  
Create some todos for Suresh:  
1. "Complete Django assignment"  
2. "Buy vegetables from market"  
3. "Call Ramesh about meeting"  
  
### Test Scenario 4: Create Second User  
  
1. Logout  
2. Register new user:  
   - Username: `ramesh`  
   - Email: `ramesh@gmail.com`  
   - Password: `ramesh123`  
3. Login as Ramesh  
4. Create different todos:  
   - "Prepare presentation for client"  
   - "Review code from Mahesh"  
  
### Test Scenario 5: Verify Isolation  
  
1. Login as `suresh` - You should see only Suresh's 3 todos  
2. Logout and login as `ramesh` - You should see only Ramesh's 2 todos  
3. Each user sees only their own todos!  
  
---  
  
## Real-World Example  
  
**Scenario:** College Project Management  
  
**Suresh (Student in Pune):**  
- Complete Python assignment  
- Study for DBMS exam  
- Submit project report  
  
**Ramesh (Student in Chennai):**  
- Finish React tutorial  
- Practice DSA questions  
- Attend workshop on Saturday  
  
**Mahesh (Working Professional in Bangalore):**  
- Prepare quarterly report  
- Review team code  
- Schedule meeting with client  
  
All three use the same todo app, but each sees only their own tasks. Privacy maintained!  
  
---  
  
## How Authentication Works  
  
### Understanding the Flow  
  
1. **Registration:**  
   - User fills form  
   - System checks if username/email already exists  
   - Creates new user with encrypted password  
   - Redirects to login  
  
2. **Login:**  
   - User enters credentials  
   - Django checks username and password  
   - If correct, creates a session  
   - User stays logged in until logout  
  
3. **Session:**  
   - Django stores session ID in browser cookie  
   - Every request includes this cookie  
   - Django knows which user is logged in  
   - `request.user` gives us the current user  
  
4. **Authorization:**  
   - `@login_required` checks if user is logged in  
   - `Todo.objects.filter(user=request.user)` gets only current user's todos  
   - `get_object_or_404(Todo, pk=pk, user=request.user)` ensures user can only access their own todos  
  
---  
  
## Security Features You Added  
  
1. **Password Hashing:**  
   - Passwords are never stored in plain text  
   - Django uses PBKDF2 algorithm  
   - Even database admin can't see passwords  
  
2. **CSRF Protection:**  
   - `{% csrf_token %}` protects against cross-site attacks  
   - Django validates every POST request  
  
3. **User Isolation:**  
   - Users can only see their own todos  
   - Users can't edit or delete others' todos  
   - `user=request.user` filter ensures this  
  
4. **Login Required:**  
   - `@login_required` decorator protects views  
   - Unauthenticated users are redirected to login  
  
---  
  
## Practice Assignment  
  
### Task 1: Add First Name and Last Name  
Modify registration to include first name and last name fields.  
  
**Hint:** User model has `first_name` and `last_name` fields  
  
### Task 2: Add User Profile Page  
Create a page showing user's profile information and total todos count.  
  
**Hint:** Use `user.todos.count()` to get todo count  
  
### Task 3: Add Password Strength Validation  
Add validation to ensure password is at least 8 characters with numbers.  
  
**Hint:** Use Python's string methods like `len()` and `isdigit()`  
  
### Task 4: Add "Remember Me" Checkbox  
Add a checkbox on login page for extended session.  
  
**Hint:** Use `request.session.set_expiry()` method  
  
---  
  
## Quick Quiz  
  
**Question 1:** What does `@login_required` decorator do?  
- A) Creates a new user  
- B) Checks if user is logged in, redirects to login if not  
- C) Logs out the user  
- D) Deletes the user account  
  
**Question 2:** What does `ForeignKey` represent in the Todo model?  
- A) A unique identifier for each todo  
- B) A relationship connecting each todo to a user  
- C) A password field  
- D) A date field  
  
**Question 3:** Why do we use `user=request.user` in todo creation?  
- A) To delete the user  
- B) To assign the todo to the currently logged-in user  
- C) To count todos  
- D) To logout the user  
  
**Question 4:** What does `authenticate()` function do?  
- A) Creates a new user  
- B) Checks if username and password are correct  
- C) Deletes a user  
- D) Logs out a user  
  
**Question 5:** What is the purpose of password hashing?  
- A) To make password longer  
- B) To store password securely so it can't be read even if database is compromised  
- C) To make login faster  
- D) To validate email  
  
---  
  
## Common Errors and Solutions  
  
### Error 1: "NOT NULL constraint failed: todos_todo.user_id"  
**Cause:** Old todos in database don't have a user assigned    
**Solution:** Delete database and migrations, start fresh (as shown in Step 2)  
  
### Error 2: "Page not found (404)" when accessing todos without login  
**Cause:** This is correct behavior! `@login_required` is working    
**Solution:** Login first, then access todos  
  
### Error 3: "Username already exists"  
**Cause:** Trying to register with an existing username    
**Solution:** Choose a different username  
  
### Error 4: "Invalid username or password"  
**Cause:** Wrong credentials or user doesn't exist    
**Solution:** Double-check username and password, or register if new user  
  
### Error 5: Can see other users' todos  
**Cause:** Forgot to add `user=request.user` filter in views    
**Solution:** Check all views have `.filter(user=request.user)`  
  
---  
  
## Key Concepts Summary  
  
### Authentication vs Authorization  
  
**Authentication:** "Who are you?"  
- Registration  
- Login  
- Session management  
  
**Authorization:** "What can you do?"  
- `@login_required` - Can you access this page?  
- `user=request.user` - Can you see/edit this data?  
  
### Django's Built-in User Model  
  
Django provides `User` model with:  
- `username`  
- `email`  
- `password` (automatically hashed)  
- `first_name`  
- `last_name`  
- `is_authenticated` (property to check if logged in)  
  
### Session Management  
  
When user logs in:  
1. Django creates a session  
2. Stores session ID in browser cookie  
3. Every request includes this cookie  
4. Django retrieves user from session  
5. Available as `request.user` in views  
  
---  
  
## What You Learned  
  
- ✓ User registration with validation  
- ✓ User login and logout  
- ✓ Session management  
- ✓ Protecting views with `@login_required`  
- ✓ Filtering data by user  
- ✓ Password hashing and security  
- ✓ User isolation and privacy  
- ✓ Django messages framework  
- ✓ Navigation bar for logged-in users  
  
---  
  
## Next Steps  
  
In **Stage 3**, we'll add:  
- Better user experience with profile pages  
- Password reset functionality  
- Email verification  
- More advanced filtering options  
  
In **Stage 4**, we'll add:  
- Todo status (Todo, In Progress, Done)  
- Priority levels (Low, Medium, High)  
- Due dates and reminders  
- Categories and tags  
  
**Excellent work completing Stage 2!** You now have a fully secure, multi-user todo application. Each user has their own private workspace!  
  
---  
  
## Quiz Answers  
  
1. **B** - Checks if user is logged in, redirects to login if not  
2. **B** - A relationship connecting each todo to a user  
3. **B** - To assign the todo to the currently logged-in user  
4. **B** - Checks if username and password are correct  
5. **B** - To store password securely so it can't be read even if database is compromised  
  
---  
  
## Testing Checklist  
  
Before moving to Stage 3, ensure:  
- [ ] You can register new users  
- [ ] You can login with correct credentials  
- [ ] Wrong password shows error  
- [ ] Duplicate username shows error  
- [ ] After login, navbar shows username  
- [ ] Each user sees only their own todos  
- [ ] Users cannot access other users' todos  
- [ ] Logout works correctly  
- [ ] Cannot access todo pages without login  
- [ ] Messages display correctly  
  
---  
