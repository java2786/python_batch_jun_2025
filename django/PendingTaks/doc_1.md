# Django Advanced Tutorial: Blog Application with File Upload, Class Based Views, Testing & Email

**Duration:** 90 minutes  
**Level:** Advanced Beginner  
**Prerequisites:** Completed Django Todo CRUD App (Stages 1-4)

---

## What You'll Build

A complete blog application where users can:
- Create profile with photo upload
- Manage blog posts using Class Based Views
- Receive email notifications when posts are published
- Test application functionality with automated tests

**Real-World Example:** Think of platforms like Medium, Dev.to, or Blogger where users write and manage articles.

---

## Table of Contents

1. [Part 1: Project Setup & Models (10 min)](#part-1-project-setup--models)
2. [Part 2: File Upload - User Profile Picture (20 min)](#part-2-file-upload---user-profile-picture)
3. [Part 3: Class Based Views - Blog CRUD (35 min)](#part-3-class-based-views---blog-crud)
4. [Part 4: Testing - Writing Test Cases (20 min)](#part-4-testing---writing-test-cases)
5. [Part 5: Django Mail - Email Notifications (15 min)](#part-5-django-mail---email-notifications)
6. [Quick Quiz](#quick-quiz)
7. [Practice Assignments](#practice-assignments)

---

## Part 1: Project Setup & Models

**Duration:** 10 minutes

### What You'll Learn
- Setting up a new Django project for blog application
- Creating models for User Profile and Blog Posts
- Understanding media file configuration

### Step 1: Create New Django Project

```bash
# Create project directory
mkdir django_blog_app
cd django_blog_app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install Django
pip install django pillow

# Create project
django-admin startproject blogproject .

# Create app
python manage.py startapp blog
```

### Step 2: Configure Settings

Open `blogproject/settings.py` and update:

```python
import os

# Add blog app to INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',  # Add this
]

# Media files configuration (for file uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files
STATIC_URL = '/static/'
```

### Step 3: Create Models

Create `blog/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
```

### Step 4: Create and Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Create superuser with these details:
- Username: `suresh`
- Email: `suresh@example.com`
- Password: `suresh123`

### Understanding the Code

**Profile Model:**
- `OneToOneField`: Each user has exactly one profile
- `ImageField`: Stores profile pictures (requires Pillow library)
- `upload_to='profile_pics/'`: Files saved in media/profile_pics/

**BlogPost Model:**
- `SlugField`: URL-friendly version of title (e.g., "my-first-blog" instead of "My First Blog")
- `ForeignKey`: Links post to author (one user can have many posts)
- `STATUS_CHOICES`: Post can be draft or published
- `get_absolute_url()`: Returns the URL to view this post

**Real-World Example:** 
Ramesh from Bangalore creates a blog profile. His photo is stored in `media/profile_pics/ramesh.jpg`. When he writes "Top 10 Python Tips", Django creates slug "top-10-python-tips" for clean URL.

---

## Part 2: File Upload - User Profile Picture

**Duration:** 20 minutes

### What You'll Learn
- Handling file uploads in Django
- Validating image files
- Displaying uploaded images in templates
- Configuring media files properly

### Step 1: Configure URLs for Media Files

Update `blogproject/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Step 2: Create Forms

Create `blog/forms.py`:

```python
from django import forms
from .models import Profile, BlogPost
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mumbai, Maharashtra'
            })
        }

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            # Validate file size (max 2MB)
            if picture.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Image file size should not exceed 2MB")
            
            # Validate file extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            import os
            ext = os.path.splitext(picture.name)[1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError("Only JPG, JPEG, PNG, and GIF files are allowed")
        
        return picture
```

### Step 3: Create Views

Create `blog/views.py`:

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, BlogPost
from .forms import ProfileForm

@login_required
def profile_view(request):
    """Display user profile"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    context = {
        'profile': profile,
    }
    return render(request, 'blog/profile.html', context)

@login_required
def profile_edit(request):
    """Edit user profile with picture upload"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'blog/profile_edit.html', context)
```

### Step 4: Create Templates

Create `blog/templates/blog/base.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Blog App{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .profile-pic {
            width: 150px;
            height: 150px;
            object-fit: cover;
            border-radius: 50%;
        }
        .profile-pic-small {
            width: 40px;
            height: 40px;
            object-fit: cover;
            border-radius: 50%;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'post_list' %}">BlogApp</a>
            <div class="navbar-nav ms-auto">
                {% if user.is_authenticated %}
                    <a class="nav-link" href="{% url 'profile_view' %}">Profile</a>
                    <a class="nav-link" href="{% url 'post_list' %}">My Posts</a>
                    <a class="nav-link" href="{% url 'logout' %}">Logout</a>
                {% else %}
                    <a class="nav-link" href="{% url 'login' %}">Login</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}

        {% block content %}
        {% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

Create `blog/templates/blog/profile.html`:

```html
{% extends 'blog/base.html' %}

{% block title %}Profile - {{ profile.user.username }}{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-4">
        <div class="card">
            <div class="card-body text-center">
                {% if profile.profile_picture %}
                    <img src="{{ profile.profile_picture.url }}" alt="Profile Picture" class="profile-pic mb-3">
                {% else %}
                    <img src="https://via.placeholder.com/150" alt="Default Profile" class="profile-pic mb-3">
                {% endif %}
                
                <h4>{{ profile.user.username }}</h4>
                <p class="text-muted">{{ profile.user.email }}</p>
                
                <a href="{% url 'profile_edit' %}" class="btn btn-primary btn-sm">Edit Profile</a>
            </div>
        </div>
    </div>
    
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">
                <h5>Profile Information</h5>
            </div>
            <div class="card-body">
                <p><strong>Location:</strong> {{ profile.location|default:"Not specified" }}</p>
                <p><strong>Bio:</strong></p>
                <p>{{ profile.bio|default:"No bio added yet." }}</p>
                <p><strong>Member Since:</strong> {{ profile.created_at|date:"F d, Y" }}</p>
            </div>
        </div>
        
        <div class="card mt-3">
            <div class="card-header">
                <h5>Recent Blog Posts</h5>
            </div>
            <div class="card-body">
                {% if profile.user.blog_posts.all %}
                    <ul class="list-group">
                    {% for post in profile.user.blog_posts.all|slice:":5" %}
                        <li class="list-group-item">
                            <a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
                            <span class="badge bg-secondary float-end">{{ post.status }}</span>
                        </li>
                    {% endfor %}
                    </ul>
                {% else %}
                    <p class="text-muted">No posts yet.</p>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

Create `blog/templates/blog/profile_edit.html`:

```html
{% extends 'blog/base.html' %}

{% block title %}Edit Profile{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">
                <h4>Edit Profile</h4>
            </div>
            <div class="card-body">
                <form method="post" enctype="multipart/form-data">
                    {% csrf_token %}
                    
                    <div class="mb-3 text-center">
                        {% if profile.profile_picture %}
                            <img src="{{ profile.profile_picture.url }}" alt="Current Profile" class="profile-pic mb-3">
                        {% else %}
                            <img src="https://via.placeholder.com/150" alt="Default Profile" class="profile-pic mb-3">
                        {% endif %}
                    </div>
                    
                    <div class="mb-3">
                        <label for="{{ form.profile_picture.id_for_label }}" class="form-label">Profile Picture</label>
                        {{ form.profile_picture }}
                        {% if form.profile_picture.errors %}
                            <div class="text-danger">{{ form.profile_picture.errors }}</div>
                        {% endif %}
                        <small class="form-text text-muted">
                            Upload JPG, JPEG, PNG, or GIF. Max size: 2MB
                        </small>
                    </div>
                    
                    <div class="mb-3">
                        <label for="{{ form.location.id_for_label }}" class="form-label">Location</label>
                        {{ form.location }}
                        {% if form.location.errors %}
                            <div class="text-danger">{{ form.location.errors }}</div>
                        {% endif %}
                    </div>
                    
                    <div class="mb-3">
                        <label for="{{ form.bio.id_for_label }}" class="form-label">Bio</label>
                        {{ form.bio }}
                        {% if form.bio.errors %}
                            <div class="text-danger">{{ form.bio.errors }}</div>
                        {% endif %}
                    </div>
                    
                    <button type="submit" class="btn btn-primary">Update Profile</button>
                    <a href="{% url 'profile_view' %}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Step 5: Create URLs

Create `blog/urls.py`:

```python
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # Auth URLs (we'll add more later)
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
```

Create `blog/templates/blog/login.html`:

```html
{% extends 'blog/base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h4>Login</h4>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    <div class="mb-3">
                        <label for="id_username" class="form-label">Username</label>
                        <input type="text" name="username" class="form-control" id="id_username" required>
                    </div>
                    <div class="mb-3">
                        <label for="id_password" class="form-label">Password</label>
                        <input type="password" name="password" class="form-control" id="id_password" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Login</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Step 6: Update Settings

Add to `blogproject/settings.py`:

```python
# Login redirect
LOGIN_REDIRECT_URL = 'profile_view'
LOGIN_URL = 'login'
```

### Step 7: Register Models in Admin

Update `blog/admin.py`:

```python
from django.contrib import admin
from .models import Profile, BlogPost

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'created_at']
    search_fields = ['user__username', 'location']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
```

### Understanding the Code

**File Upload Key Points:**

1. **Form enctype:** `enctype="multipart/form-data"` is mandatory for file uploads
2. **request.FILES:** Contains uploaded files (separate from request.POST)
3. **ImageField:** Uses Pillow library to validate images
4. **upload_to:** Specifies subdirectory within MEDIA_ROOT
5. **File Validation:** Check size and extension in clean_profile_picture()

**Media Configuration:**
- MEDIA_ROOT: Filesystem path where uploaded files are stored
- MEDIA_URL: URL that serves media files
- In production, use cloud storage (AWS S3, Cloudinary)

**Real-World Example:**
Mahesh from Pune uploads his profile picture "mahesh_profile.jpg". Django:
1. Validates it's under 2MB and is a valid image
2. Saves to `media/profile_pics/mahesh_profile.jpg`
3. Stores path in database: `profile_pics/mahesh_profile.jpg`
4. Displays using: `{{ profile.profile_picture.url }}`

### Testing File Upload

```bash
python manage.py runserver
```

1. Visit: http://127.0.0.1:8000/login/
2. Login with: suresh / suresh123
3. Visit: http://127.0.0.1:8000/profile/
4. Click "Edit Profile"
5. Upload a profile picture (test with any image under 2MB)
6. Check media/profile_pics/ folder for uploaded file

---

## Part 3: Class Based Views - Blog CRUD

**Duration:** 35 minutes

### What You'll Learn
- Understanding Class Based Views (CBVs)
- Using Django's generic views (ListView, DetailView, CreateView, UpdateView, DeleteView)
- Mixins for authentication and permissions
- Automatic slug generation

### Why Class Based Views?

**Function Based Views (What you know):**
```python
def post_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})
```

**Class Based Views (More powerful):**
```python
class PostListView(ListView):
    model = BlogPost
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
```

Benefits: Less code, reusable, built-in pagination, forms handling.

### Step 1: Update Forms

Add to `blog/forms.py`:

```python
from django.utils.text import slugify

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter blog post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your blog content here...'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Auto-generate slug from title if not exists
        if not instance.slug:
            instance.slug = slugify(instance.title)
            
            # Ensure slug is unique
            original_slug = instance.slug
            counter = 1
            while BlogPost.objects.filter(slug=instance.slug).exists():
                instance.slug = f"{original_slug}-{counter}"
                counter += 1
        
        # Set published_at when status changes to published
        if instance.status == 'published' and not instance.published_at:
            from django.utils import timezone
            instance.published_at = timezone.now()
        
        if commit:
            instance.save()
        return instance
```

### Step 2: Create Class Based Views

Update `blog/views.py` (add these imports and classes):

```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils import timezone

# List all blog posts
class PostListView(LoginRequiredMixin, ListView):
    model = BlogPost
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        # Show only current user's posts
        return BlogPost.objects.filter(author=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_posts'] = self.get_queryset().count()
        context['published_count'] = self.get_queryset().filter(status='published').count()
        context['draft_count'] = self.get_queryset().filter(status='draft').count()
        return context

# View single blog post
class PostDetailView(LoginRequiredMixin, DetailView):
    model = BlogPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

# Create new blog post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Blog post created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Post'
        context['button_text'] = 'Create Post'
        return context

# Update existing blog post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        # Only post author can update
        post = self.get_object()
        return self.request.user == post.author
    
    def form_valid(self, form):
        messages.success(self.request, 'Blog post updated successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Post'
        context['button_text'] = 'Update Post'
        return context

# Delete blog post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        # Only post author can delete
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Blog post deleted successfully!')
        return super().delete(request, *args, **kwargs)
```

### Step 3: Create Templates for Blog Posts

Create `blog/templates/blog/post_list.html`:

```html
{% extends 'blog/base.html' %}

{% block title %}My Blog Posts{% endblock %}

{% block content %}
<div class="row mb-4">
    <div class="col-md-8">
        <h2>My Blog Posts</h2>
    </div>
    <div class="col-md-4 text-end">
        <a href="{% url 'post_create' %}" class="btn btn-primary">Create New Post</a>
    </div>
</div>

<div class="row mb-3">
    <div class="col-md-4">
        <div class="card text-center">
            <div class="card-body">
                <h5 class="card-title">{{ total_posts }}</h5>
                <p class="card-text">Total Posts</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-center">
            <div class="card-body">
                <h5 class="card-title text-success">{{ published_count }}</h5>
                <p class="card-text">Published</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-center">
            <div class="card-body">
                <h5 class="card-title text-warning">{{ draft_count }}</h5>
                <p class="card-text">Drafts</p>
            </div>
        </div>
    </div>
</div>

{% if posts %}
    {% for post in posts %}
    <div class="card mb-3">
        <div class="card-body">
            <div class="row">
                <div class="col-md-10">
                    <h5 class="card-title">
                        <a href="{% url 'post_detail' post.slug %}">{{ post.title }}</a>
                        {% if post.status == 'draft' %}
                            <span class="badge bg-warning">Draft</span>
                        {% else %}
                            <span class="badge bg-success">Published</span>
                        {% endif %}
                    </h5>
                    <p class="card-text text-muted">
                        {{ post.content|truncatewords:30 }}
                    </p>
                    <small class="text-muted">
                        Created: {{ post.created_at|date:"M d, Y" }} | 
                        Updated: {{ post.updated_at|date:"M d, Y" }}
                        {% if post.published_at %}
                            | Published: {{ post.published_at|date:"M d, Y" }}
                        {% endif %}
                    </small>
                </div>
                <div class="col-md-2 text-end">
                    <a href="{% url 'post_update' post.slug %}" class="btn btn-sm btn-outline-primary">Edit</a>
                    <a href="{% url 'post_delete' post.slug %}" class="btn btn-sm btn-outline-danger">Delete</a>
                </div>
            </div>
        </div>
    </div>
    {% endfor %}
    
    {% if is_paginated %}
    <nav>
        <ul class="pagination justify-content-center">
            {% if page_obj.has_previous %}
                <li class="page-item">
                    <a class="page-link" href="?page=1">First</a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ page_obj.previous_page_number }}">Previous</a>
                </li>
            {% endif %}
            
            <li class="page-item active">
                <span class="page-link">Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}</span>
            </li>
            
            {% if page_obj.has_next %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ page_obj.next_page_number }}">Next</a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}">Last</a>
                </li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}
{% else %}
    <div class="alert alert-info">
        <h5>No blog posts yet!</h5>
        <p>Start writing your first blog post.</p>
        <a href="{% url 'post_create' %}" class="btn btn-primary">Create Your First Post</a>
    </div>
{% endif %}
{% endblock %}
```

Create `blog/templates/blog/post_detail.html`:

```html
{% extends 'blog/base.html' %}

{% block title %}{{ post.title }}{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8 mx-auto">
        <div class="card">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h2>{{ post.title }}</h2>
                    {% if post.status == 'draft' %}
                        <span class="badge bg-warning">Draft</span>
                    {% else %}
                        <span class="badge bg-success">Published</span>
                    {% endif %}
                </div>
                
                <div class="text-muted mb-3">
                    <small>
                        By <strong>{{ post.author.username }}</strong> | 
                        Created: {{ post.created_at|date:"F d, Y" }}
                        {% if post.published_at %}
                            | Published: {{ post.published_at|date:"F d, Y" }}
                        {% endif %}
                    </small>
                </div>
                
                <hr>
                
                <div class="content">
                    {{ post.content|linebreaks }}
                </div>
                
                <hr>
                
                <div class="mt-4">
                    {% if user == post.author %}
                        <a href="{% url 'post_update' post.slug %}" class="btn btn-primary">Edit Post</a>
                        <a href="{% url 'post_delete' post.slug %}" class="btn btn-danger">Delete Post</a>
                    {% endif %}
                    <a href="{% url 'post_list' %}" class="btn btn-secondary">Back to Posts</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

Create `blog/templates/blog/post_form.html`:

```html
{% extends 'blog/base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8 mx-auto">
        <div class="card">
            <div class="card-header">
                <h4>{{ title }}</h4>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    
                    <div class="mb-3">
                        <label for="{{ form.title.id_for_label }}" class="form-label">Title</label>
                        {{ form.title }}
                        {% if form.title.errors %}
                            <div class="text-danger">{{ form.title.errors }}</div>
                        {% endif %}
                    </div>
                    
                    <div class="mb-3">
                        <label for="{{ form.content.id_for_label }}" class="form-label">Content</label>
                        {{ form.content }}
                        {% if form.content.errors %}
                            <div class="text-danger">{{ form.content.errors }}</div>
                        {% endif %}
                    </div>
                    
                    <div class="mb-3">
                        <label for="{{ form.status.id_for_label }}" class="form-label">Status</label>
                        {{ form.status }}
                        {% if form.status.errors %}
                            <div class="text-danger">{{ form.status.errors }}</div>
                        {% endif %}
                    </div>
                    
                    <button type="submit" class="btn btn-primary">{{ button_text }}</button>
                    <a href="{% url 'post_list' %}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

Create `blog/templates/blog/post_confirm_delete.html`:

```html
{% extends 'blog/base.html' %}

{% block title %}Delete Post{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-6 mx-auto">
        <div class="card">
            <div class="card-header bg-danger text-white">
                <h4>Confirm Delete</h4>
            </div>
            <div class="card-body">
                <p>Are you sure you want to delete the post:</p>
                <h5>"{{ post.title }}"</h5>
                <p class="text-muted">This action cannot be undone.</p>
                
                <form method="post">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-danger">Yes, Delete</button>
                    <a href="{% url 'post_list' %}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Step 4: Update URLs

Update `blog/urls.py`:

```python
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Profile URLs
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # Blog Post URLs (Class Based Views)
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Auth URLs
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
```

### Understanding Class Based Views

**1. ListView:**
- Displays list of objects
- Built-in pagination support
- `get_queryset()`: Customize which objects to show
- `get_context_data()`: Add extra context

**2. DetailView:**
- Shows single object detail
- Uses slug or pk to find object
- Automatic 404 if object not found

**3. CreateView:**
- Displays form to create object
- `form_valid()`: Called when form is valid
- Automatically saves object to database

**4. UpdateView:**
- Displays form with existing data
- Updates object on submission
- Can use mixins to restrict access

**5. DeleteView:**
- Asks for confirmation before deleting
- Redirects to success_url after deletion

**Mixins:**
- `LoginRequiredMixin`: Requires user to be logged in
- `UserPassesTestMixin`: Custom permission check via test_func()

**Real-World Example:**
Dinesh from Chennai creates a blog post "Django Tips for Beginners":
1. Clicks "Create New Post" → PostCreateView
2. Form auto-generates slug: "django-tips-for-beginners"
3. Submits form → form_valid() sets author to Dinesh
4. Redirects to post list → PostListView shows all Dinesh's posts

### Testing Class Based Views

```bash
python manage.py runserver
```

Test flow:
1. Login at http://127.0.0.1:8000/login/
2. Create new post at http://127.0.0.1:8000/post/create/
3. View post list at http://127.0.0.1:8000/
4. Click post title to view detail
5. Edit and delete posts

---

## Part 4: Testing - Writing Test Cases

**Duration:** 20 minutes

### What You'll Learn
- Why testing is important
- Writing unit tests for models
- Testing views and forms
- Testing file uploads
- Running and interpreting test results

### Why Write Tests?

Without tests:
- Manual testing after each change
- Risk of breaking existing features
- Fear of refactoring code

With tests:
- Automated verification
- Confidence in code changes
- Documentation of how code should work

**Real-World Example:** Flipkart adds new payment method. Tests ensure existing checkout, cart, and orders still work correctly.

### Step 1: Create Test File

Create `blog/tests.py`:

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import Profile, BlogPost
from .forms import ProfileForm, BlogPostForm
import os

class ProfileModelTest(TestCase):
    """Test cases for Profile model"""
    
    def setUp(self):
        """Run before each test method"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio',
            location='Mumbai'
        )
    
    def test_profile_creation(self):
        """Test profile is created correctly"""
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.location, 'Mumbai')
        self.assertEqual(str(self.profile), "testuser's Profile")
    
    def test_profile_without_picture(self):
        """Test profile can exist without picture"""
        self.assertFalse(self.profile.profile_picture)
    
    def tearDown(self):
        """Run after each test method"""
        # Clean up any uploaded files
        if self.profile.profile_picture:
            if os.path.exists(self.profile.profile_picture.path):
                os.remove(self.profile.profile_picture.path)

class BlogPostModelTest(TestCase):
    """Test cases for BlogPost model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='mukesh',
            password='mukesh123'
        )
        self.post = BlogPost.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='This is test content',
            status='draft'
        )
    
    def test_post_creation(self):
        """Test blog post is created correctly"""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author.username, 'mukesh')
        self.assertEqual(self.post.status, 'draft')
    
    def test_post_str_method(self):
        """Test string representation of post"""
        self.assertEqual(str(self.post), 'Test Post')
    
    def test_post_absolute_url(self):
        """Test get_absolute_url method"""
        url = self.post.get_absolute_url()
        self.assertEqual(url, '/post/test-post/')
    
    def test_post_ordering(self):
        """Test posts are ordered by created_at descending"""
        post2 = BlogPost.objects.create(
            title='Second Post',
            slug='second-post',
            author=self.user,
            content='Second content'
        )
        posts = BlogPost.objects.all()
        self.assertEqual(posts[0], post2)  # Newest first
        self.assertEqual(posts[1], self.post)

class ProfileFormTest(TestCase):
    """Test cases for ProfileForm"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='formtest',
            password='formtest123'
        )
    
    def test_valid_form(self):
        """Test form with valid data"""
        form_data = {
            'bio': 'I am a Django developer',
            'location': 'Pune'
        }
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_with_large_file(self):
        """Test form rejects files larger than 2MB"""
        # Create a fake large file (3MB)
        large_file = SimpleUploadedFile(
            "large_image.jpg",
            b"x" * (3 * 1024 * 1024),  # 3MB of data
            content_type="image/jpeg"
        )
        
        form_data = {'bio': 'Test', 'location': 'Chennai'}
        form_files = {'profile_picture': large_file}
        form = ProfileForm(data=form_data, files=form_files)
        
        self.assertFalse(form.is_valid())
        self.assertIn('profile_picture', form.errors)
    
    def test_form_with_invalid_extension(self):
        """Test form rejects invalid file extensions"""
        invalid_file = SimpleUploadedFile(
            "document.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        
        form_data = {'bio': 'Test', 'location': 'Delhi'}
        form_files = {'profile_picture': invalid_file}
        form = ProfileForm(data=form_data, files=form_files)
        
        self.assertFalse(form.is_valid())

class BlogPostFormTest(TestCase):
    """Test cases for BlogPostForm"""
    
    def test_slug_auto_generation(self):
        """Test slug is auto-generated from title"""
        user = User.objects.create_user(username='slugtest', password='pass123')
        form_data = {
            'title': 'My First Blog Post',
            'content': 'Content here',
            'status': 'draft'
        }
        form = BlogPostForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        post = form.save(commit=False)
        post.author = user
        post.save()
        
        self.assertEqual(post.slug, 'my-first-blog-post')
    
    def test_unique_slug_generation(self):
        """Test duplicate titles get unique slugs"""
        user = User.objects.create_user(username='uniquetest', password='pass123')
        
        # Create first post
        BlogPost.objects.create(
            title='Duplicate Title',
            slug='duplicate-title',
            author=user,
            content='First content'
        )
        
        # Try to create second post with same title
        form_data = {
            'title': 'Duplicate Title',
            'content': 'Second content',
            'status': 'draft'
        }
        form = BlogPostForm(data=form_data)
        post = form.save(commit=False)
        post.author = user
        post.save()
        
        self.assertEqual(post.slug, 'duplicate-title-1')

class ProfileViewTest(TestCase):
    """Test cases for Profile views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='viewtest',
            password='viewtest123'
        )
        self.profile = Profile.objects.create(user=self.user)
    
    def test_profile_view_requires_login(self):
        """Test profile view redirects if not logged in"""
        response = self.client.get(reverse('profile_view'))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertIn('/login/', response.url)
    
    def test_profile_view_when_logged_in(self):
        """Test profile view works when logged in"""
        self.client.login(username='viewtest', password='viewtest123')
        response = self.client.get(reverse('profile_view'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'viewtest')
        self.assertTemplateUsed(response, 'blog/profile.html')
    
    def test_profile_edit_post_request(self):
        """Test profile edit with POST request"""
        self.client.login(username='viewtest', password='viewtest123')
        
        response = self.client.post(reverse('profile_edit'), {
            'bio': 'Updated bio',
            'location': 'Bangalore'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check profile was updated
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated bio')
        self.assertEqual(self.profile.location, 'Bangalore')

class BlogPostViewTest(TestCase):
    """Test cases for BlogPost views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='nitesh',
            password='nitesh123'
        )
        self.post = BlogPost.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='Test content',
            status='published'
        )
    
    def test_post_list_view(self):
        """Test post list view shows user's posts"""
        self.client.login(username='nitesh', password='nitesh123')
        response = self.client.get(reverse('post_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertEqual(len(response.context['posts']), 1)
    
    def test_post_detail_view(self):
        """Test post detail view displays post"""
        self.client.login(username='nitesh', password='nitesh123')
        response = self.client.get(
            reverse('post_detail', kwargs={'slug': 'test-post'})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'Test content')
    
    def test_post_create_view(self):
        """Test creating new post"""
        self.client.login(username='nitesh', password='nitesh123')
        
        response = self.client.post(reverse('post_create'), {
            'title': 'New Post',
            'content': 'New content',
            'status': 'draft'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(BlogPost.objects.count(), 2)
        
        new_post = BlogPost.objects.get(title='New Post')
        self.assertEqual(new_post.author, self.user)
        self.assertEqual(new_post.slug, 'new-post')
    
    def test_post_update_view(self):
        """Test updating existing post"""
        self.client.login(username='nitesh', password='nitesh123')
        
        response = self.client.post(
            reverse('post_update', kwargs={'slug': 'test-post'}),
            {
                'title': 'Updated Title',
                'content': 'Updated content',
                'status': 'published'
            }
        )
        
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
    
    def test_post_delete_view(self):
        """Test deleting post"""
        self.client.login(username='nitesh', password='nitesh123')
        
        response = self.client.post(
            reverse('post_delete', kwargs={'slug': 'test-post'})
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(BlogPost.objects.count(), 0)
    
    def test_unauthorized_user_cannot_edit(self):
        """Test other users cannot edit post"""
        other_user = User.objects.create_user(
            username='hitesh',
            password='hitesh123'
        )
        self.client.login(username='hitesh', password='hitesh123')
        
        response = self.client.get(
            reverse('post_update', kwargs={'slug': 'test-post'})
        )
        
        self.assertEqual(response.status_code, 403)  # Forbidden

class IntegrationTest(TestCase):
    """Integration tests for complete workflows"""
    
    def test_complete_blog_workflow(self):
        """Test complete flow: register -> create profile -> create post"""
        # Create user
        user = User.objects.create_user(
            username='workflow',
            password='workflow123'
        )
        
        # Login
        self.client.login(username='workflow', password='workflow123')
        
        # Create profile
        Profile.objects.create(
            user=user,
            bio='Integration test bio',
            location='Hyderabad'
        )
        
        # Create blog post
        response = self.client.post(reverse('post_create'), {
            'title': 'Integration Test Post',
            'content': 'Testing complete workflow',
            'status': 'published'
        })
        
        # Verify post was created
        self.assertEqual(BlogPost.objects.count(), 1)
        post = BlogPost.objects.first()
        self.assertEqual(post.title, 'Integration Test Post')
        self.assertEqual(post.author, user)
        
        # Verify can view post
        response = self.client.get(
            reverse('post_detail', kwargs={'slug': post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Integration Test Post')
```

### Step 2: Run Tests

```bash
# Run all tests
python manage.py test

# Run specific test class
python manage.py test blog.tests.ProfileModelTest

# Run specific test method
python manage.py test blog.tests.ProfileModelTest.test_profile_creation

# Run with verbose output
python manage.py test --verbosity=2

# Keep test database for inspection
python manage.py test --keepdb
```

### Understanding Test Output

**Successful test:**
```
..........
----------------------------------------------------------------------
Ran 10 tests in 2.145s

OK
```

**Failed test:**
```
F.........
======================================================================
FAIL: test_profile_creation (blog.tests.ProfileModelTest)
----------------------------------------------------------------------
AssertionError: 'testuser' != 'wronguser'

----------------------------------------------------------------------
Ran 10 tests in 2.145s

FAILED (failures=1)
```

### Test Best Practices

1. **Use setUp() and tearDown():**
   - setUp(): Create test data before each test
   - tearDown(): Clean up after each test

2. **Test one thing per method:**
   - Bad: test_everything()
   - Good: test_profile_creation(), test_profile_update()

3. **Use descriptive names:**
   - Bad: test1(), test2()
   - Good: test_user_cannot_edit_others_posts()

4. **Test both success and failure:**
   - Test valid data works
   - Test invalid data is rejected

5. **Use assertions effectively:**
   - assertEqual(a, b): Check equality
   - assertTrue(x): Check if True
   - assertFalse(x): Check if False
   - assertIn(item, list): Check membership
   - assertContains(response, text): Check text in HTTP response

**Real-World Example:**
LIC insurance system tests:
- Model tests: Verify policy calculations are correct
- Form tests: Ensure invalid dates are rejected
- View tests: Check only policy holder can view their policy
- Integration tests: Complete flow from registration to policy purchase

---

## Part 5: Django Mail - Email Notifications

**Duration:** 15 minutes

### What You'll Learn
- Configuring email settings in Django
- Sending emails when posts are published
- Using Django signals for automatic actions
- Testing email functionality

### Why Email Notifications?

**Use Cases:**
- Welcome emails for new users
- Password reset links
- Blog post published notifications
- Order confirmations (e-commerce)
- Account verification

**Real-World Example:** When Kamlesh publishes a blog post on Medium, subscribers receive email notification.

### Step 1: Configure Email Settings

Add to `blogproject/settings.py`:

```python
# Email Configuration (Development - Console Backend)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For production with Gmail (commented for now):
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your_email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your_app_password'  # Use App Password, not regular password
# DEFAULT_FROM_EMAIL = 'your_email@gmail.com'
```

**Note:** In development, we use `console` backend which prints emails to terminal instead of sending them.

### Step 2: Create Email Utility Functions

Create `blog/utils.py`:

```python
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_post_published_email(post):
    """
    Send email notification when blog post is published
    """
    subject = f'New Blog Post Published: {post.title}'
    
    # HTML email content
    html_message = render_to_string('blog/emails/post_published.html', {
        'post': post,
        'author': post.author,
    })
    
    # Plain text version (fallback)
    plain_message = strip_tags(html_message)
    
    # In real app, send to subscribers list
    # For demo, send to author
    recipient_list = [post.author.email]
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@blogapp.com',
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=False,
    )

def send_welcome_email(user):
    """
    Send welcome email to new users
    """
    subject = 'Welcome to BlogApp!'
    message = f'''
    Hi {user.username},
    
    Welcome to BlogApp! We're excited to have you as part of our community.
    
    Start by creating your profile and publishing your first blog post.
    
    Happy blogging!
    
    The BlogApp Team
    '''
    
    send_mail(
        subject=subject,
        message=message,
        from_email='noreply@blogapp.com',
        recipient_list=[user.email],
        fail_silently=False,
    )

def send_bulk_notification(subject, message, recipient_list):
    """
    Send same email to multiple recipients efficiently
    """
    messages = []
    for recipient in recipient_list:
        messages.append((
            subject,
            message,
            'noreply@blogapp.com',
            [recipient]
        ))
    
    send_mass_mail(messages, fail_silently=False)
```

### Step 3: Create Email Template

Create `blog/templates/blog/emails/post_published.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background-color: #007bff;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .content {
            padding: 20px;
            background-color: #f8f9fa;
        }
        .button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 15px;
        }
        .footer {
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>New Blog Post Published!</h1>
        </div>
        
        <div class="content">
            <h2>{{ post.title }}</h2>
            
            <p><strong>By:</strong> {{ author.username }}</p>
            <p><strong>Published:</strong> {{ post.published_at|date:"F d, Y" }}</p>
            
            <p>{{ post.content|truncatewords:50 }}</p>
            
            <a href="{{ post.get_absolute_url }}" class="button">Read Full Post</a>
        </div>
        
        <div class="footer">
            <p>You're receiving this email because you're subscribed to {{ author.username }}'s blog.</p>
            <p>&copy; 2024 BlogApp. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
```

### Step 4: Use Django Signals

Create `blog/signals.py`:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import BlogPost, Profile
from .utils import send_post_published_email, send_welcome_email

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create profile when user is created
    Send welcome email
    """
    if created:
        Profile.objects.create(user=instance)
        if instance.email:
            send_welcome_email(instance)

@receiver(post_save, sender=BlogPost)
def notify_post_published(sender, instance, created, **kwargs):
    """
    Send email notification when post status changes to published
    """
    if not created:  # Only for updates, not new posts
        if instance.status == 'published' and instance.published_at:
            # Check if this is first time being published
            old_post = BlogPost.objects.filter(pk=instance.pk).first()
            if old_post and old_post.status != 'published':
                send_post_published_email(instance)
```

### Step 5: Register Signals

Update `blog/apps.py`:

```python
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        import blog.signals
```

### Step 6: Update Views to Trigger Emails

Signals handle automatic emails, but you can also send manually.

Add to `blog/views.py`:

```python
from .utils import send_post_published_email

# Add this method to PostUpdateView class:
def form_valid(self, form):
    response = super().form_valid(form)
    
    # Check if status changed to published
    if form.instance.status == 'published' and not form.instance.published_at:
        from django.utils import timezone
        form.instance.published_at = timezone.now()
        form.instance.save()
        
        # Send email notification
        send_post_published_email(form.instance)
        
        messages.success(
            self.request, 
            'Blog post published and notification sent!'
        )
    else:
        messages.success(self.request, 'Blog post updated successfully!')
    
    return response
```

### Step 7: Test Email Functionality

```bash
python manage.py runserver
```

1. Login and create a new blog post
2. Set status to "Published"
3. Check your terminal/console - you'll see the email content printed there
4. Example output:

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: New Blog Post Published: Django Testing Guide
From: noreply@blogapp.com
To: suresh@example.com
Date: Wed, 15 Nov 2024 10:30:00 -0000

New Blog Post Published!

Django Testing Guide

By: suresh
Published: November 15, 2024

Testing is an essential part of Django development...
```

### Understanding Django Signals

**What are Signals?**
Signals allow certain senders to notify receivers when specific actions occur.

**Common Signals:**
- `post_save`: After model is saved
- `pre_save`: Before model is saved
- `post_delete`: After model is deleted
- `pre_delete`: Before model is deleted

**Signal Components:**
1. **Sender:** Model that sends signal (e.g., BlogPost)
2. **Receiver:** Function that handles signal (decorated with @receiver)
3. **Signal Type:** When to trigger (e.g., post_save)

**Real-World Example:**
Indian Railways ticket booking:
- Signal: post_save on Ticket model
- Action: Send confirmation email with ticket details
- Action: Send SMS with PNR number
- Action: Update seat availability

### Gmail Configuration (Production)

To use real Gmail for sending emails:

1. **Enable 2-Factor Authentication** in your Gmail account
2. **Generate App Password:**
   - Go to Google Account → Security
   - Enable 2-Step Verification
   - Generate App Password for "Mail"
3. **Update settings.py:**

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_16_char_app_password'
DEFAULT_FROM_EMAIL = 'your_email@gmail.com'
```

4. **Test:**

```python
from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test email from Django.',
    'your_email@gmail.com',
    ['recipient@example.com'],
    fail_silently=False,
)
```

### Common Email Errors and Solutions

**Error 1: SMTPAuthenticationError**
```
Solution: Use App Password instead of regular Gmail password
```

**Error 2: Connection refused**
```
Solution: Check EMAIL_PORT (587 for TLS, 465 for SSL)
```

**Error 3: Email not sent but no error**
```
Solution: Set fail_silently=False to see actual errors
```

**Error 4: HTML not rendering**
```
Solution: Make sure email client supports HTML, provide plain text fallback
```

---

## Common Errors and Solutions

### Error 1: File Upload Not Working

**Error:**
```
The submitted file is empty.
```

**Solution:**
- Ensure form has `enctype="multipart/form-data"`
- Check MEDIA_URL and MEDIA_ROOT in settings
- Verify folder permissions for media directory

### Error 2: Class Based View Not Found

**Error:**
```
AttributeError: 'PostListView' object has no attribute 'object'
```

**Solution:**
- Use correct generic view (ListView, not DetailView)
- Ensure context_object_name is set
- Check get_queryset() returns queryset, not list

### Error 3: Test Database Not Created

**Error:**
```
Got an error creating the test database: permission denied
```

**Solution:**
```bash
# Use --keepdb flag
python manage.py test --keepdb

# Or grant database permissions
# For PostgreSQL:
ALTER USER myuser CREATEDB;
```

### Error 4: Signal Not Triggering

**Error:**
Emails not being sent automatically

**Solution:**
- Verify signals.py is imported in apps.py ready() method
- Check sender model matches exactly
- Use print statements to debug signal execution

### Error 5: Slug Collision

**Error:**
```
IntegrityError: duplicate key value violates unique constraint
```

**Solution:**
Already handled in BlogPostForm.save() method with counter increment

---

## Quick Quiz

Test your understanding with these questions:

### Question 1
What is the correct way to configure media files in Django?

**A)** Set MEDIA_URL = '/media/' only  
**B)** Set MEDIA_ROOT = 'media/' only  
**C)** Set both MEDIA_URL and MEDIA_ROOT, and add static() in urls.py  
**D)** Media files work automatically without configuration

<details>
<summary>Click to see answer</summary>

**Answer: C**

Explanation: You need both MEDIA_URL (URL prefix) and MEDIA_ROOT (filesystem path). Additionally, in development, you must add `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` to urlpatterns to serve media files.

</details>

### Question 2
Which Class Based View should you use to display a list of blog posts?

**A)** DetailView  
**B)** ListView  
**C)** CreateView  
**D)** FormView

<details>
<summary>Click to see answer</summary>

**Answer: B**

Explanation: ListView is designed to display a list of objects. DetailView shows single object, CreateView handles object creation, and FormView handles form submission without a model.

</details>

### Question 3
What does the `LoginRequiredMixin` do in Class Based Views?

**A)** Displays a login form  
**B)** Creates a new user account  
**C)** Redirects non-authenticated users to login page  
**D)** Logs out the current user

<details>
<summary>Click to see answer</summary>

**Answer: C**

Explanation: LoginRequiredMixin checks if user is authenticated. If not, it redirects them to the login page (specified by LOGIN_URL in settings).

</details>

### Question 4
In Django testing, what does `setUp()` method do?

**A)** Runs after all tests complete  
**B)** Runs before each individual test method  
**C)** Runs only once before all tests  
**D)** Runs when a test fails

<details>
<summary>Click to see answer</summary>

**Answer: B**

Explanation: setUp() runs before each test method in the test class. This ensures each test starts with a fresh, predictable state. tearDown() runs after each test.

</details>

### Question 5
Which email backend should you use during development?

**A)** smtp.EmailBackend  
**B)** console.EmailBackend  
**C)** file.EmailBackend  
**D)** memory.EmailBackend

<details>
<summary>Click to see answer</summary>

**Answer: B**

Explanation: console.EmailBackend prints emails to the terminal/console, which is perfect for development. smtp.EmailBackend actually sends emails through an SMTP server, which should be used in production.

</details>

---

## Practice Assignments

### Assignment 1: Add Comment System (Easy)
**Duration:** 30 minutes

Create a comment system for blog posts:
- Model: Comment (post, author, content, created_at)
- Users can add comments on published posts
- Display comments under blog post detail
- Only comment author can delete their comment

**Hints:**
- Use ForeignKey to link Comment to BlogPost
- Add comments section in post_detail.html
- Create CommentCreateView or use function-based view

### Assignment 2: Add Tags to Posts (Medium)
**Duration:** 45 minutes

Implement tagging system:
- Model: Tag (name, slug)
- Many-to-Many relationship between BlogPost and Tag
- Display tags on post list and detail
- Filter posts by tag
- Create tag cloud showing popular tags

**Hints:**
- Use ManyToManyField in BlogPost model
- Use django-taggit library or create custom implementation
- Add tag filtering in PostListView.get_queryset()

### Assignment 3: Add Rich Text Editor (Medium)
**Duration:** 30 minutes

Replace plain textarea with rich text editor:
- Install django-ckeditor
- Configure CKEditor in settings
- Update BlogPost model to use RichTextField
- Test formatting (bold, italic, lists, links)

**Hints:**
```python
# Install
pip install django-ckeditor

# settings.py
INSTALLED_APPS = ['ckeditor', ...]

# models.py
from ckeditor.fields import RichTextField
content = RichTextField()
```

### Assignment 4: Add Email Subscription (Hard)
**Duration:** 60 minutes

Allow users to subscribe to blog updates:
- Model: Subscriber (email, is_active, subscribed_at)
- Subscription form on blog homepage
- Send email to all subscribers when new post is published
- Unsubscribe link in emails

**Hints:**
- Create SubscriberCreateView
- Update send_post_published_email() to send to all subscribers
- Generate unique unsubscribe token using UUID
- Create unsubscribe view with token verification

### Assignment 5: Add Post Statistics Dashboard (Hard)
**Duration:** 60 minutes

Create analytics dashboard for authors:
- Total views per post (add view_count field)
- Most popular posts
- Monthly post creation chart
- Draft vs Published ratio
- Implement view counter (increment on each post view)

**Hints:**
- Add view_count = models.PositiveIntegerField(default=0) to BlogPost
- Use Django aggregation: `BlogPost.objects.aggregate(Sum('view_count'))`
- Create custom template tag for statistics
- Use Chart.js or Plotly for visualization

### Assignment 6: Write More Tests (Medium)
**Duration:** 45 minutes

Expand test coverage:
- Test file upload validation (test various file sizes and types)
- Test unauthorized access to edit/delete (UserPassesTestMixin)
- Test email sending in signals
- Test pagination in ListView
- Aim for 80% code coverage

**Hints:**
```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test blog
coverage report
coverage html
```

---

## Summary

Congratulations! You've completed the Django Advanced Blog Application tutorial covering:

**Part 1: Project Setup & Models**
- Media file configuration
- Profile and BlogPost models
- One-to-One and Foreign Key relationships

**Part 2: File Upload**
- ImageField for profile pictures
- File validation (size, extension)
- Serving media files in development

**Part 3: Class Based Views**
- ListView, DetailView, CreateView, UpdateView, DeleteView
- LoginRequiredMixin and UserPassesTestMixin
- Automatic slug generation
- Form handling in CBVs

**Part 4: Testing**
- Model, Form, and View tests
- setUp() and tearDown() methods
- Integration testing
- Running and interpreting test results

**Part 5: Django Mail**
- Email configuration (console and SMTP)
- send_mail() and send_mass_mail()
- HTML email templates
- Django signals for automatic actions

**Key Takeaways:**
1. File uploads require proper media configuration
2. Class Based Views reduce code and add functionality
3. Tests ensure code reliability and prevent regressions
4. Signals enable automatic actions without tight coupling
5. Email notifications enhance user engagement

**Real-World Applications:**
- Blogging platforms (Medium, Dev.to)
- Content management systems
- News portals
- Documentation sites
- Company blogs

Keep practicing and building! The best way to master Django is through hands-on projects.

Happy coding!