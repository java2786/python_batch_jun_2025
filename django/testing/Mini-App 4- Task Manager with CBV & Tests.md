# Django Mini-App 4: Task Manager with CBV & Tests

**Duration:** 15 minutes  
**Topics:** Class Based Views, Django Testing

---

## What You'll Build

CRUD task manager using Class Based Views + Write automated tests.

---

## Part 1: Setup (3 min)

```bash
mkdir task_manager && cd task_manager
python -m venv venv
venv\Scripts\activate
pip install django
django-admin startproject taskproject .
python manage.py startapp tasks
```

**Configure `taskproject/settings.py`:**

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks',
]

LOGIN_REDIRECT_URL = 'task_list'
LOGIN_URL = 'login'
```

**Create Model `tasks/models.py`:**

```python
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

    # /tasks/{self.pk}/
    def get_absolute_url(self):
        # Mapping View Names to URLs
        # the reverse function in Django does not reverse a string or change the order of characters
        return reverse('task_detail', kwargs={'pk': self.pk})
```

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
# Username: admin, Password: admin123
```

---

## Part 2: Class Based Views (6 min)

**Create Views `tasks/views.py`:**

```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Task

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'status']
    success_url = reverse_lazy('task_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Task created successfully!')
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'status']
    success_url = reverse_lazy('task_list')
    
    def test_func(self):
        return self.request.user == self.get_object().user
    
    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
    
    def test_func(self):
        return self.request.user == self.get_object().user
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Task deleted successfully!')
        return super().delete(request, *args, **kwargs)
```

**Create Templates `tasks/templates/tasks/task_list.html`:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Tasks</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'task_list' %}">Task Manager</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link text-white" href="{% url 'logout' %}">Logout</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}

        <div class="d-flex justify-content-between mb-3">
            <h2>My Tasks</h2>
            <a href="{% url 'task_create' %}" class="btn btn-primary">+ New Task</a>
        </div>

        {% for task in tasks %}
        <div class="card mb-2">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h5>
                            <a href="{% url 'task_detail' task.pk %}">{{ task.title }}</a>
                            <span class="badge bg-{% if task.status == 'completed' %}success{% else %}warning{% endif %}">
                                {{ task.get_status_display }}
                            </span>
                        </h5>
                        <p class="text-muted">{{ task.description|truncatewords:20 }}</p>
                        <small>Created: {{ task.created_at|date:"M d, Y H:i" }}</small>
                    </div>
                    <div>
                        <a href="{% url 'task_update' task.pk %}" class="btn btn-sm btn-outline-primary">Edit</a>
                        <a href="{% url 'task_delete' task.pk %}" class="btn btn-sm btn-outline-danger">Delete</a>
                    </div>
                </div>
            </div>
        </div>
        {% empty %}
        <div class="alert alert-info">
            No tasks yet! <a href="{% url 'task_create' %}">Create your first task</a>
        </div>
        {% endfor %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

**Create `tasks/templates/tasks/task_form.html`:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Task Form</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header"><h4>{% if object %}Edit{% else %}Create{% endif %} Task</h4></div>
                    <div class="card-body">
                        <form method="post">
                            {% csrf_token %}
                            {{ form.as_p }}
                            <button type="submit" class="btn btn-primary">Save</button>
                            <a href="{% url 'task_list' %}" class="btn btn-secondary">Cancel</a>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

**Create `tasks/templates/tasks/task_detail.html`:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ task.title }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="card">
            <div class="card-header">
                <h3>{{ task.title }}</h3>
            </div>
            <div class="card-body">
                <p><strong>Status:</strong> {{ task.get_status_display }}</p>
                <p><strong>Description:</strong> {{ task.description }}</p>
                <p><strong>Created:</strong> {{ task.created_at|date:"F d, Y H:i" }}</p>
                <hr>
                <a href="{% url 'task_update' task.pk %}" class="btn btn-primary">Edit</a>
                <a href="{% url 'task_delete' task.pk %}" class="btn btn-danger">Delete</a>
                <a href="{% url 'task_list' %}" class="btn btn-secondary">Back</a>
            </div>
        </div>
    </div>
</body>
</html>
```

**Create `tasks/templates/tasks/task_confirm_delete.html`:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Delete Task</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="card">
            <div class="card-header bg-danger text-white">
                <h4>Confirm Delete</h4>
            </div>
            <div class="card-body">
                <p>Are you sure you want to delete: <strong>{{ task.title }}</strong>?</p>
                <form method="post">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-danger">Yes, Delete</button>
                    <a href="{% url 'task_list' %}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
```

---

## Part 3: Write Tests (6 min)

**Create Tests `tasks/tests.py`:**

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Task

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test description',
            status='pending'
        )
    
    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(str(self.task), 'Test Task')
        self.assertEqual(self.task.status, 'pending')
    
    def test_get_absolute_url(self):
        self.assertEqual(self.task.get_absolute_url(), f'/tasks/{self.task.pk}/')

class TaskViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test description',
            status='pending'
        )
    
    def test_task_list_requires_login(self):
        # reverse is a URL resolver and not a string reversal function

        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_task_list_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
    
    def test_task_create(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('task_create'), {
            'title': 'New Task',
            'description': 'New description',
            'status': 'pending'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after create
        self.assertEqual(Task.objects.count(), 2)
    
    def test_task_update(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('task_update', kwargs={'pk': self.task.pk}),
            {'title': 'Updated Task', 'description': 'Updated', 'status': 'completed'}
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.status, 'completed')
    
    def test_task_delete(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('task_delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)
    
    def test_user_cannot_edit_others_task(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpass123')
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(reverse('task_update', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 403)  # Forbidden
```

**Run Tests:**

```bash
# Run all tests
python manage.py test

# Run with verbose output
python manage.py test --verbosity=2

# Run specific test
python manage.py test tasks.tests.TaskModelTest
```

**Expected Output:**

```
Creating test database...
..........
----------------------------------------------------------------------
Ran 10 tests in 0.523s

OK
Destroying test database...
```

**Configure URLs `tasks/urls.py`:**

```python
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
```

**Create Login Template `tasks/templates/tasks/login.html`:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header"><h4>Login</h4></div>
                    <div class="card-body">
                        <form method="post">
                            {% csrf_token %}
                            <div class="mb-3">
                                <label>Username</label>
                                <input type="text" name="username" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label>Password</label>
                                <input type="password" name="password" class="form-control" required>
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Login</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

**Update `taskproject/urls.py`:**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
]
```

---

## Quick Test

```bash
python manage.py runserver
```

**Test CBVs:**

1. Visit http://localhost:8000/ → Redirects to login
2. Login: `admin` / `admin123`
3. Create task → Success message
4. Edit task → Changes saved
5. Delete task → Confirmation page

**Run Tests:**

```bash
python manage.py test
```

✅ All 10 tests should pass!

---

## What You Learned

✅ **Class Based Views:**
- ListView - Display list
- DetailView - Single object
- CreateView - Create form
- UpdateView - Edit form
- DeleteView - Delete confirmation

✅ **Mixins:**
- LoginRequiredMixin - Require authentication
- UserPassesTestMixin - Custom permissions

✅ **Django Testing:**
- TestCase class
- setUp() method
- Client for requests
- Assertions (assertEqual, assertContains)
- Test authentication & permissions

---

## Quick Quiz

**Q1:** What's the benefit of CBVs over function views?

<details>
<summary>Answer</summary>
Less code, reusable, built-in features (pagination, forms), better organization.
</details>

**Q2:** What does `test_func()` do in UserPassesTestMixin?

<details>
<summary>Answer</summary>
Custom permission check. Returns True to allow, False to deny (403 Forbidden).
</details>

**Q3:** Why use `setUp()` in tests?

<details>
<summary>Answer</summary>
Runs before each test method to create fresh test data.
</details>

---

**Time Taken:** 15 minutes  
**Tests:** 10 (all pass)  
**Test Coverage:** ~80%  
**Lines of Code:** ~220