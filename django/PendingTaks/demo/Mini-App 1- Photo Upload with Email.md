# Django Mini-App 1: Photo Upload with Email

**Duration:** 15 minutes  
**Topics:** File Upload, Django Mail

---

## What You'll Build

Upload a profile photo → System validates file → Sends email confirmation with photo attached.

---

## Part 1: Setup (3 min)

```bash
# Create project
mkdir photo_uploader && cd photo_uploader
python -m venv venv
venv\Scripts\activate  # Windows
pip install django pillow
django-admin startproject photoproject .
python manage.py startapp uploader
```

**Configure `photoproject/settings.py`:**

```python
import os

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'uploader',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email Configuration (Console Backend for Testing)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**Create Model `uploader/models.py`:**

```python
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
```

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
# Username: admin, Password: admin123
```

---

## Part 2: File Upload with Validation (6 min)

**Create Form `uploader/forms.py`:**

```python
from django import forms
from .models import Profile

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
        }
    
    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            # Validate file size (max 2MB)
            if photo.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Image size should not exceed 2MB")
            
            # Validate file extension
            import os
            ext = os.path.splitext(photo.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError("Only JPG and PNG files are allowed")
        return photo
```

**Create View `uploader/views.py`:**

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PhotoUploadForm
from .models import Profile

@login_required
def upload_photo(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            
            # Send email (Part 3)
            from .utils import send_upload_email
            send_upload_email(request.user, profile)
            
            messages.success(request, 'Photo uploaded and email sent!')
            return redirect('upload_photo')
    else:
        form = PhotoUploadForm(instance=profile)
    
    return render(request, 'uploader/upload.html', {'form': form, 'profile': profile})
```

**Create Template `uploader/templates/uploader/upload.html`:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Upload Photo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header"><h4>Upload Profile Photo</h4></div>
                    <div class="card-body">
                        {% if messages %}
                            {% for message in messages %}
                                <div class="alert alert-{{ message.tags }}">{{ message }}</div>
                            {% endfor %}
                        {% endif %}
                        
                        {% if profile and profile.photo %}
                            <div class="text-center mb-3">
                                <img src="{{ profile.photo.url }}" width="150" class="rounded-circle">
                                <p class="mt-2">Uploaded: {{ profile.uploaded_at|date:"M d, Y H:i" }}</p>
                            </div>
                        {% endif %}
                        
                        <form method="post" enctype="multipart/form-data">
                            {% csrf_token %}
                            <div class="mb-3">
                                <label>Select Photo (Max 2MB, JPG/PNG only)</label>
                                {{ form.photo }}
                                {% if form.photo.errors %}
                                    <div class="text-danger">{{ form.photo.errors }}</div>
                                {% endif %}
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Upload Photo</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

---

## Part 3: Send Email with Attachment (6 min)

**Create `uploader/utils.py`:**

```python
from django.core.mail import EmailMessage
from django.conf import settings

def send_upload_email(user, profile):
    subject = f'Photo Uploaded Successfully - {user.username}'
    message = f'''
    Hi {user.username},
    
    Your profile photo has been uploaded successfully!
    
    Upload Time: {profile.uploaded_at.strftime("%B %d, %Y at %H:%M")}
    
    Thank you for using our service!
    
    Best regards,
    Photo Uploader Team
    '''
    
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email='noreply@photouploader.com',
        to=[user.email],
    )
    
    # Attach the uploaded photo
    if profile.photo:
        email.attach_file(profile.photo.path)
    
    email.send(fail_silently=False)
```

**Configure URLs `uploader/urls.py`:**

```python
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.upload_photo, name='upload_photo'),
    path('login/', auth_views.LoginView.as_view(template_name='uploader/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
```

**Create Login Template `uploader/templates/uploader/login.html`:**

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

**Update `photoproject/urls.py`:**

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Update `photoproject/settings.py`:**

```python
LOGIN_REDIRECT_URL = 'upload_photo'
LOGIN_URL = 'login'
```

---

## Quick Test

```bash
python manage.py runserver
```

**Test Steps:**

1. Visit http://localhost:8000/
2. Login with: `admin` / `admin123`
3. Upload a photo (JPG/PNG, under 2MB)
4. Click "Upload Photo"
5. Check terminal - you'll see email output:

```
Content-Type: text/plain; charset="utf-8"
Subject: Photo Uploaded Successfully - admin
From: noreply@photouploader.com
To: admin@example.com
Content-Type: image/jpeg
Content-Disposition: attachment; filename="photo_abc123.jpg"

Hi admin,

Your profile photo has been uploaded successfully!
...
```

**Test Validation:**

1. Try uploading file > 2MB → Error message
2. Try uploading .txt file → Error message
3. Try uploading valid JPG → Success!

---

## What You Learned

✅ **File Upload:**
- ImageField for photo storage
- File validation (size, extension)
- Media files configuration

✅ **Django Mail:**
- EmailMessage class
- Attach files to email
- Console backend for testing

✅ **Best Practices:**
- Form validation
- User feedback with messages
- Login required decorator

---

## Quick Quiz

**Q1:** What's the difference between `EmailMessage` and `send_mail()`?

<details>
<summary>Answer</summary>
`EmailMessage` allows attachments and more control. `send_mail()` is simpler but can't attach files.
</details>

**Q2:** Where are uploaded files stored?

<details>
<summary>Answer</summary>
In `MEDIA_ROOT` directory (media/photos/ in this case).
</details>

**Q3:** How to send real emails in production?

<details>
<summary>Answer</summary>
Change `EMAIL_BACKEND` to SMTP and configure EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD.
</details>

---

**Time Taken:** 15 minutes  
**Files Created:** 7  
**Lines of Code:** ~150