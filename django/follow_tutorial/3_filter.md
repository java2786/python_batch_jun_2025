# Django Todo App - Stage 3: Advanced User Features & Filtering  
  
**Prerequisites:** Completed Stage 1 (Basic CRUD) and Stage 2 (User Authentication)  
  
---  
  
## What You'll Build  
  
In this stage, you'll add:  
- **User Profile Page** - View user information and statistics  
- **Search Functionality** - Search todos by title or description  
- **Filter by Status** - View all, completed, or pending todos  
- **Todo Statistics** - Total, completed, and pending counts  
- **Edit Profile** - Update user information  
- **Change Password** - Secure password update  
  
**Real-World Example:**    
Mahesh has 50 todos in his list. He wants to quickly find todos related to "Django", see only pending tasks, or view his profile with statistics. After Stage 3, he can do all of this easily!  
  
---  
  
## Part 1: Add Search Functionality   
  
### Why Search?  
  
When you have many todos, finding a specific one becomes difficult. Search helps you quickly locate todos by title or description.  
  
### Step 1: Update Todo List View  
  
Open `todos/views.py` and modify the `todo_list` view:  
  
```python  
from django.db.models import Q  
  
@login_required  
def todo_list(request):  
    todos = Todo.objects.filter(user=request.user)  
      
    # Search functionality  
    search_query = request.GET.get('search', '')  
    if search_query:  
        todos = todos.filter(  
            Q(title__icontains=search_query) |   
            Q(description__icontains=search_query)  
        )  
      
    # Filter by status  
    status_filter = request.GET.get('status', 'all')  
    if status_filter == 'completed':  
        todos = todos.filter(completed=True)  
    elif status_filter == 'pending':  
        todos = todos.filter(completed=False)  
      
    # Statistics  
    total_todos = Todo.objects.filter(user=request.user).count()  
    completed_todos = Todo.objects.filter(user=request.user, completed=True).count()  
    pending_todos = Todo.objects.filter(user=request.user, completed=False).count()  
      
    context = {  
        'todos': todos,  
        'search_query': search_query,  
        'status_filter': status_filter,  
        'total_todos': total_todos,  
        'completed_todos': completed_todos,  
        'pending_todos': pending_todos,  
    }  
      
    return render(request, 'todos/todo_list.html', context)  
```  
  
**Understanding the Code:**  
  
1. **Q Objects:**  
   - `Q` allows complex queries with OR conditions  
   - `Q(title__icontains=search_query)` - searches in title  
   - `|` means OR  
   - `icontains` means case-insensitive search  
  
2. **GET Parameters:**  
   - `request.GET.get('search', '')` - gets search query from URL  
   - Default is empty string if not provided  
  
3. **Statistics:**  
   - `.count()` - counts total records  
   - Separate counts for total, completed, and pending  
  
### Step 2: Update Todo List Template  
  
Replace `todos/templates/todos/todo_list.html`:  
  
```html  
{% extends 'todos/base.html' %}  
  
{% block content %}  
<h1>My Todo List</h1>  
  
<!-- Statistics Dashboard -->  
<div style="display: flex; justify-content: space-around; margin: 20px 0; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">  
    <div style="text-align: center;">  
        <h3 style="color: #007bff; margin: 0;">{{ total_todos }}</h3>  
        <p style="color: #666; margin: 5px 0;">Total</p>  
    </div>  
    <div style="text-align: center;">  
        <h3 style="color: #28a745; margin: 0;">{{ completed_todos }}</h3>  
        <p style="color: #666; margin: 5px 0;">Completed</p>  
    </div>  
    <div style="text-align: center;">  
        <h3 style="color: #ffc107; margin: 0;">{{ pending_todos }}</h3>  
        <p style="color: #666; margin: 5px 0;">Pending</p>  
    </div>  
</div>  
  
<!-- Search and Filter Form -->  
<form method="GET" style="margin: 20px 0; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">  
    <div style="display: flex; gap: 10px; align-items: flex-end;">  
        <div style="flex: 1;">  
            <label for="search">Search Todos:</label>  
            <input type="text" id="search" name="search" value="{{ search_query }}"   
                   placeholder="Search by title or description..."   
                   style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">  
        </div>  
          
        <div>  
            <label for="status">Filter by Status:</label>  
            <select id="status" name="status" style="padding: 10px; border: 1px solid #ddd; border-radius: 5px;">  
                <option value="all" {% if status_filter == 'all' %}selected{% endif %}>All Todos</option>  
                <option value="pending" {% if status_filter == 'pending' %}selected{% endif %}>Pending</option>  
                <option value="completed" {% if status_filter == 'completed' %}selected{% endif %}>Completed</option>  
            </select>  
        </div>  
          
        <button type="submit" class="btn">Apply</button>  
        <a href="{% url 'todo_list' %}" class="btn btn-danger">Clear</a>  
    </div>  
</form>  
  
<a href="{% url 'todo_create' %}" class="btn" style="margin-bottom: 20px;">Add New Todo</a>  
  
<!-- Display Search Results Info -->  
{% if search_query %}  
<p style="color: #666; margin: 10px 0;">  
    Showing results for "<strong>{{ search_query }}</strong>" - Found {{ todos|length }} todo(s)  
</p>  
{% endif %}  
  
<!-- Todos List -->  
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
        {% if search_query %}  
            <p style="text-align: center; color: #999; margin-top: 50px;">  
                No todos found matching "{{ search_query }}". Try a different search term.  
            </p>  
        {% else %}  
            <p style="text-align: center; color: #999; margin-top: 50px;">  
                No todos yet. Create your first todo!  
            </p>  
        {% endif %}  
    {% endif %}  
</div>  
{% endblock %}  
```  
  
---  
  
## Part 2: Create User Profile   
  
### Step 3: Create Profile View  
  
Add this view to `todos/views.py`:  
  
```python  
@login_required  
def profile_view(request):  
    user = request.user  
      
    # Get user statistics  
    total_todos = Todo.objects.filter(user=user).count()  
    completed_todos = Todo.objects.filter(user=user, completed=True).count()  
    pending_todos = Todo.objects.filter(user=user, completed=False).count()  
      
    # Calculate completion percentage  
    if total_todos > 0:  
        completion_percentage = (completed_todos / total_todos) * 100  
    else:  
        completion_percentage = 0  
      
    # Get recent todos  
    recent_todos = Todo.objects.filter(user=user).order_by('-created_at')[:5]  
      
    context = {  
        'total_todos': total_todos,  
        'completed_todos': completed_todos,  
        'pending_todos': pending_todos,  
        'completion_percentage': round(completion_percentage, 1),  
        'recent_todos': recent_todos,  
    }  
      
    return render(request, 'todos/profile.html', context)  
```  
  
### Step 4: Create Edit Profile View  
  
Add this view to `todos/views.py`:  
  
```python  
@login_required  
def edit_profile_view(request):  
    if request.method == 'POST':  
        user = request.user  
        user.first_name = request.POST.get('first_name')  
        user.last_name = request.POST.get('last_name')  
        user.email = request.POST.get('email')  
        user.save()  
          
        messages.success(request, 'Profile updated successfully!')  
        return redirect('profile')  
      
    return render(request, 'todos/edit_profile.html')  
```  
  
### Step 5: Create Change Password View  
  
Add this view to `todos/views.py`:  
  
```python  
from django.contrib.auth import update_session_auth_hash  
  
@login_required  
def change_password_view(request):  
    if request.method == 'POST':  
        current_password = request.POST.get('current_password')  
        new_password = request.POST.get('new_password')  
        confirm_password = request.POST.get('confirm_password')  
          
        user = request.user  
          
        # Check if current password is correct  
        if not user.check_password(current_password):  
            messages.error(request, 'Current password is incorrect!')  
            return render(request, 'todos/change_password.html')  
          
        # Check if new passwords match  
        if new_password != confirm_password:  
            messages.error(request, 'New passwords do not match!')  
            return render(request, 'todos/change_password.html')  
          
        # Check password length  
        if len(new_password) < 6:  
            messages.error(request, 'Password must be at least 6 characters long!')  
            return render(request, 'todos/change_password.html')  
          
        # Update password  
        user.set_password(new_password)  
        user.save()  
          
        # Keep user logged in after password change  
        update_session_auth_hash(request, user)  
          
        messages.success(request, 'Password changed successfully!')  
        return redirect('profile')  
      
    return render(request, 'todos/change_password.html')  
```  
  
### Step 6: Update URLs  
  
Open `todos/urls.py` and add new URLs:  
  
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
      
    # Profile URLs  
    path('profile/', views.profile_view, name='profile'),  
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),  
    path('profile/change-password/', views.change_password_view, name='change_password'),  
]  
```  
  
### Step 7: Update Navbar in Base Template  
  
Update the navbar section in `todos/templates/todos/base.html`:  
  
```html  
{% if user.is_authenticated %}  
<div class="navbar">  
    <h2>Todo App</h2>  
    <div>  
        <span>Welcome, {{ user.username }}!</span>  
        <a href="{% url 'todo_list' %}">My Todos</a>  
        <a href="{% url 'profile' %}">Profile</a>  
        <a href="{% url 'logout' %}">Logout</a>  
    </div>  
</div>  
{% endif %}  
```  
  
---  
  
## Part 3: Create Profile Templates   
  
### Step 8: Create Profile Template  
  
Create `todos/templates/todos/profile.html`:  
  
```html  
{% extends 'todos/base.html' %}  
  
{% block content %}  
<h1>User Profile</h1>  
  
<!-- User Information Card -->  
<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 30px;">  
    <div style="display: flex; justify-content: space-between; align-items: center;">  
        <div>  
            <h2 style="color: #007bff; margin: 0 0 10px 0;">  
                {% if user.first_name %}  
                    {{ user.first_name }} {{ user.last_name }}  
                {% else %}  
                    {{ user.username }}  
                {% endif %}  
            </h2>  
            <p style="margin: 5px 0; color: #666;"><strong>Username:</strong> {{ user.username }}</p>  
            <p style="margin: 5px 0; color: #666;"><strong>Email:</strong> {{ user.email }}</p>  
            <p style="margin: 5px 0; color: #666;"><strong>Member Since:</strong> {{ user.date_joined|date:"d M Y" }}</p>  
        </div>  
        <div>  
            <a href="{% url 'edit_profile' %}" class="btn">Edit Profile</a>  
            <a href="{% url 'change_password' %}" class="btn btn-danger">Change Password</a>  
        </div>  
    </div>  
</div>  
  
<!-- Statistics Dashboard -->  
<h2>Todo Statistics</h2>  
<div style="display: flex; justify-content: space-around; margin: 20px 0; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">  
    <div style="text-align: center;">  
        <h3 style="color: #007bff; margin: 0; font-size: 36px;">{{ total_todos }}</h3>  
        <p style="color: #666; margin: 10px 0;">Total Todos</p>  
    </div>  
    <div style="text-align: center;">  
        <h3 style="color: #28a745; margin: 0; font-size: 36px;">{{ completed_todos }}</h3>  
        <p style="color: #666; margin: 10px 0;">Completed</p>  
    </div>  
    <div style="text-align: center;">  
        <h3 style="color: #ffc107; margin: 0; font-size: 36px;">{{ pending_todos }}</h3>  
        <p style="color: #666; margin: 10px 0;">Pending</p>  
    </div>  
    <div style="text-align: center;">  
        <h3 style="color: #17a2b8; margin: 0; font-size: 36px;">{{ completion_percentage }}%</h3>  
        <p style="color: #666; margin: 10px 0;">Completion Rate</p>  
    </div>  
</div>  
  
<!-- Progress Bar -->  
<div style="margin: 30px 0;">  
    <p style="color: #666; margin-bottom: 10px;"><strong>Overall Progress:</strong></p>  
    <div style="background-color: #e9ecef; height: 30px; border-radius: 15px; overflow: hidden;">  
        <div style="background-color: #28a745; height: 100%; width: {{ completion_percentage }}%;   
                    display: flex; align-items: center; justify-content: center; color: white;   
                    font-weight: bold; transition: width 0.3s ease;">  
            {% if completion_percentage > 0 %}{{ completion_percentage }}%{% endif %}  
        </div>  
    </div>  
</div>  
  
<!-- Recent Todos -->  
<h2>Recent Todos</h2>  
{% if recent_todos %}  
    <div style="margin-top: 20px;">  
        {% for todo in recent_todos %}  
        <div style="border-left: 4px solid {% if todo.completed %}#28a745{% else %}#ffc107{% endif %};   
                    padding: 10px 15px; margin-bottom: 10px; background-color: #f8f9fa; border-radius: 5px;">  
            <strong style="color: {% if todo.completed %}#155724{% else %}#333{% endif %};">  
                {{ todo.title }}  
            </strong>  
            {% if todo.completed %}  
                <span style="color: green; font-size: 12px; margin-left: 10px;">✓ Completed</span>  
            {% endif %}  
            <br>  
            <small style="color: #999;">{{ todo.created_at|date:"d M Y, h:i A" }}</small>  
        </div>  
        {% endfor %}  
    </div>  
{% else %}  
    <p style="color: #999; text-align: center; padding: 20px;">No todos yet. Start creating!</p>  
{% endif %}  
  
<div style="text-align: center; margin-top: 30px;">  
    <a href="{% url 'todo_list' %}" class="btn">View All Todos</a>  
</div>  
{% endblock %}  
```  
  
### Step 9: Create Edit Profile Template  
  
Create `todos/templates/todos/edit_profile.html`:  
  
```html  
{% extends 'todos/base.html' %}  
  
{% block content %}  
<h1>Edit Profile</h1>  
  
<form method="POST">  
    {% csrf_token %}  
      
    <label for="first_name">First Name:</label>  
    <input type="text" id="first_name" name="first_name" value="{{ user.first_name }}" required>  
      
    <label for="last_name">Last Name:</label>  
    <input type="text" id="last_name" name="last_name" value="{{ user.last_name }}" required>  
      
    <label for="email">Email:</label>  
    <input type="email" id="email" name="email" value="{{ user.email }}" required>  
      
    <p style="color: #666; font-size: 14px; margin: 10px 0;">  
        Note: You cannot change your username. To change password, use the "Change Password" option.  
    </p>  
      
    <button type="submit" class="btn">Update Profile</button>  
    <a href="{% url 'profile' %}" class="btn btn-danger">Cancel</a>  
</form>  
{% endblock %}  
```  
  
### Step 10: Create Change Password Template  
  
Create `todos/templates/todos/change_password.html`:  
  
```html  
{% extends 'todos/base.html' %}  
  
{% block content %}  
<h1>Change Password</h1>  
  
<div style="background-color: #fff3cd; border: 1px solid #ffc107; padding: 15px; border-radius: 5px; margin-bottom: 20px;">  
    <strong>Important:</strong> After changing your password, you will remain logged in. Make sure to remember your new password!  
</div>  
  
<form method="POST">  
    {% csrf_token %}  
      
    <label for="current_password">Current Password:</label>  
    <input type="password" id="current_password" name="current_password" required>  
      
    <label for="new_password">New Password:</label>  
    <input type="password" id="new_password" name="new_password" required>  
      
    <label for="confirm_password">Confirm New Password:</label>  
    <input type="password" id="confirm_password" name="confirm_password" required>  
      
    <p style="color: #666; font-size: 14px; margin: 10px 0;">  
        Password must be at least 6 characters long.  
    </p>  
      
    <button type="submit" class="btn">Change Password</button>  
    <a href="{% url 'profile' %}" class="btn btn-danger">Cancel</a>  
</form>  
{% endblock %}  
```  
  
---  
  
## Part 4: Test the Application   
  
### Test Scenario 1: Search Functionality  
  
1. Login as any user  
2. Create several todos:  
   - "Complete Django tutorial"  
   - "Buy vegetables from market"  
   - "Learn Python Django framework"  
   - "Call Ramesh about meeting"  
   - "Django project deployment"  
  
3. **Test Search:**  
   - Search for "Django" - Should show 3 todos  
   - Search for "market" - Should show 1 todo  
   - Search for "xyz" - Should show "No todos found"  
  
### Test Scenario 2: Filter by Status  
  
1. Mark some todos as completed  
2. Use filter dropdown:  
   - Select "All Todos" - Shows all todos  
   - Select "Pending" - Shows only incomplete todos  
   - Select "Completed" - Shows only completed todos  
  
### Test Scenario 3: Combined Search and Filter  
  
1. Search for "Django"  
2. Filter by "Completed"  
3. Should show only completed todos containing "Django"  
  
### Test Scenario 4: User Profile  
  
1. Click "Profile" in navbar  
2. You should see:  
   - Your username and email  
   - Total todos count  
   - Completed and pending counts  
   - Completion percentage  
   - Progress bar  
   - Recent 5 todos  
  
### Test Scenario 5: Edit Profile  
  
1. Click "Edit Profile"  
2. Update:  
   - First Name: "Suresh"  
   - Last Name: "Kumar"  
   - Email: "suresh.kumar@gmail.com"  
3. Click "Update Profile"  
4. Verify changes in profile page  
  
### Test Scenario 6: Change Password  
  
1. Click "Change Password"  
2. Enter:  
   - Current Password: (your current password)  
   - New Password: "newpass123"  
   - Confirm: "newpass123"  
3. Click "Change Password"  
4. Should see success message  
5. Logout and login with new password to verify  
  
---  
  
## Real-World Example  
  
**Scenario:** Dinesh is a Software Developer in Chennai  
  
**His Usage:**  
  
**Morning:**  
- Opens todo app  
- Sees dashboard: 25 total, 15 completed, 10 pending (60% completion)  
- Searches "bug" to find all bug-related tasks  
- Filters by "Pending" to see what needs attention  
  
**During Work:**  
- Completes tasks and marks them done  
- Progress bar moves from 60% to 68%  
- Creates new todo: "Review Mahesh's code"  
  
**Evening:**  
- Checks profile to see productivity  
- Notices 17 completed tasks today  
- Feels accomplished seeing 68% completion rate  
  
**Profile Update:**  
- Updates email to work email  
- Changes password for security  
  
---  
  
## Understanding Q Objects  
  
### What are Q Objects?  
  
`Q` objects allow complex database queries with AND/OR logic.  
  
### Simple Examples:  
  
**Example 1: Search in title OR description**  
```python  
Q(title__icontains='Django') | Q(description__icontains='Django')  
```  
Finds todos where either title or description contains "Django"  
  
**Example 2: Multiple conditions**  
```python  
Q(completed=True) & Q(title__icontains='urgent')  
```  
Finds todos that are completed AND contain "urgent"  
  
**Example 3: Complex query**  
```python  
Q(completed=False) & (Q(title__icontains='bug') | Q(description__icontains='bug'))  
```  
Finds pending todos that have "bug" in title or description  
  
---  
  
## Statistics and Calculations  
  
### Counting Records  
  
```python  
# Total count  
total = Todo.objects.filter(user=request.user).count()  
  
# Conditional count  
completed = Todo.objects.filter(user=request.user, completed=True).count()  
```  
  
### Percentage Calculation  
  
```python  
if total > 0:  
    percentage = (completed / total) * 100  
else:  
    percentage = 0  
  
# Round to 1 decimal place  
percentage = round(percentage, 1)  
```  
  
### Practical Example:  
  
Nitesh has:  
- Total todos: 20  
- Completed: 15  
- Pending: 5  
  
Calculation:  
- Completion rate = (15 / 20) × 100 = 75%  
- Progress bar shows 75% filled  
  
---  
  
## Practice Assignment  
  
### Task 1: Add Date Filter  
Add ability to filter todos by creation date (today, this week, this month).  
  
**Hint:** Use Django's date filters like `created_at__date=today`  
  
### Task 2: Add Category Field  
Add a category field to todos (Work, Personal, Shopping, etc.) and filter by category.  
  
**Hint:** Use `CharField` with `choices` parameter  
  
### Task 3: Add Export Feature  
Create a button to export all todos to a text file.  
  
**Hint:** Use Python's file writing capabilities  
  
### Task 4: Add Sort Options  
Allow users to sort todos by title, date, or completion status.  
  
**Hint:** Use `.order_by()` with different fields  
  
### Task 5: Add Todo Count in Navbar  
Show total pending todos count in the navbar.  
  
**Hint:** Add context processor or pass count in every view  
  
---  
  
## Quick Quiz  
  
**Question 1:** What does the `Q` object allow you to do?  
- A) Delete records  
- B) Create complex queries with OR logic  
- C) Update multiple records  
- D) Count records  
  
**Question 2:** What does `icontains` lookup do?  
- A) Exact match search  
- B) Case-sensitive search  
- C) Case-insensitive search  
- D) Number search  
  
**Question 3:** How do you get URL parameters in Django?  
- A) `request.POST.get()`  
- B) `request.GET.get()`  
- C) `request.PARAMS.get()`  
- D) `request.URL.get()`  
  
**Question 4:** What does `update_session_auth_hash()` do?  
- A) Logs out the user  
- B) Keeps user logged in after password change  
- C) Creates new session  
- D) Deletes session  
  
**Question 5:** What happens if you don't use `update_session_auth_hash()` after changing password?  
- A) Nothing  
- B) User gets logged out automatically  
- C) Password doesn't change  
- D) Account gets deleted  
  
---  
  
## Common Errors and Solutions  
  
### Error 1: "Q object is not defined"  
**Cause:** Forgot to import Q    
**Solution:** Add `from django.db.models import Q` at the top of views.py  
  
### Error 2: Search returns no results even though todos exist  
**Cause:** Typo in search query or wrong field name    
**Solution:** Check spelling, ensure using `icontains` (case-insensitive)  
  
### Error 3: Statistics showing zero for all counts  
**Cause:** Not filtering by current user    
**Solution:** Always use `.filter(user=request.user)` in all queries  
  
### Error 4: User gets logged out after password change  
**Cause:** Forgot `update_session_auth_hash()`    
**Solution:** Add `update_session_auth_hash(request, user)` after password change  
  
### Error 5: Filter dropdown not working  
**Cause:** Form method is POST instead of GET    
**Solution:** Use `<form method="GET">` for search and filter forms  
  
---  
  
## Performance Tips  
  
### Tip 1: Use select_related for ForeignKeys  
```python  
todos = Todo.objects.filter(user=request.user).select_related('user')  
```  
Reduces database queries  
  
### Tip 2: Use Pagination for Large Lists  
When you have 100+ todos, load them in pages:  
```python  
from django.core.paginator import Paginator  
  
paginator = Paginator(todos, 10)  # 10 todos per page  
page_number = request.GET.get('page')  
page_obj = paginator.get_page(page_number)  
```  
  
### Tip 3: Index Database Fields  
For fields you search frequently, add database index:  
```python  
class Todo(models.Model):  
    title = models.CharField(max_length=200, db_index=True)  
```  
  
---  
  
## Security Considerations  
  
### 1. Password Security  
- Minimum 6 characters (increase to 8+ in production)  
- Add complexity requirements (uppercase, numbers, symbols)  
- Use Django's built-in password validators  
  
### 2. User Data Isolation  
- Always filter by `user=request.user`  
- Never trust user input for user IDs  
- Use `get_object_or_404()` with user filter  
  
### 3. Input Validation  
- Validate all form inputs  
- Sanitize search queries  
- Prevent SQL injection (Django handles this)  
  
### 4. Session Security  
- Use `update_session_auth_hash()` after password change  
- Set session timeout in settings  
- Use HTTPS in production  
  
---  
  
## What You Learned  
  
- ✓ Search functionality with Q objects  
- ✓ Complex database queries  
- ✓ Filtering by multiple criteria  
- ✓ GET parameters in URLs  
- ✓ User profile page with statistics  
- ✓ Calculating percentages  
- ✓ Edit profile functionality  
- ✓ Secure password change  
- ✓ Session management after password change  
- ✓ User experience improvements  
- ✓ Dashboard with statistics  
- ✓ Progress visualization  
  
---  
  
## Next Steps  
  
In **Stage 4**, we'll add:  
- **Status Field** - Todo, In Progress, Completed  
- **Priority Levels** - Low, Medium, High, Critical  
- **Due Dates** - Set deadlines for todos  
- **Overdue Notifications** - Visual indicators for overdue tasks  
- **Better Styling** - Professional UI with colors  
- **Bulk Actions** - Delete or complete multiple todos at once  
  
**Excellent work completing Stage 3!** Your todo app now has professional features like search, filtering, and user profiles. Users can efficiently manage their tasks and track their productivity.  
  
---  
  
## Quiz Answers  
  
1. **B** - Create complex queries with OR logic  
2. **C** - Case-insensitive search  
3. **B** - `request.GET.get()`  
4. **B** - Keeps user logged in after password change  
5. **B** - User gets logged out automatically  
  
---  
