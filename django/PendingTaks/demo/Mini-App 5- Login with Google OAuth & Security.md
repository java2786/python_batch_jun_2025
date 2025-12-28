# Django Mini-App 5: Login with Google OAuth & Security  
  
**Duration:** 15 minutes    
**Topics:** Django OAuth (Google), Security in Django  
  
---  
  
## What You'll Build  
  
Google login + Production-ready security settings.  
  
---  
  
## Part 1: Setup (3 min)  
  
```bash  
mkdir oauth_login && cd oauth_login  
python -m venv venv  
venv\Scripts\activate  
pip install django django-allauth requests jwt  
django-admin startproject oauthproject .  
python manage.py startapp accounts  
```  
  
**Configure `oauthproject/settings.py`:**  
  
```python  
INSTALLED_APPS = [  
    'django.contrib.admin',  
    'django.contrib.auth',  
    'django.contrib.contenttypes',  
    'django.contrib.sessions',  
    'django.contrib.messages',  
    'django.contrib.staticfiles',  
    'django.contrib.sites',  
      
    # django-allauth  
    'allauth',  
    'allauth.account',  
    'allauth.socialaccount',  
    'allauth.socialaccount.providers.google',  
      
    'accounts',  
]  
  
MIDDLEWARE = [  
    'django.middleware.security.SecurityMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',  
    'django.middleware.common.CommonMiddleware',  
    'django.middleware.csrf.CsrfViewMiddleware',  
    'django.contrib.auth.middleware.AuthenticationMiddleware',  
    'django.contrib.messages.middleware.MessageMiddleware',  
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  
    'allauth.account.middleware.AccountMiddleware',  
]  
  
AUTHENTICATION_BACKENDS = [  
    'django.contrib.auth.backends.ModelBackend',  
    'allauth.account.auth_backends.AuthenticationBackend',  
]  
  
SITE_ID = 1  
  
LOGIN_REDIRECT_URL = '/dashboard/'  
LOGOUT_REDIRECT_URL = '/'  
  
# Allauth settings  
ACCOUNT_EMAIL_REQUIRED = True  
ACCOUNT_USERNAME_REQUIRED = False  
ACCOUNT_AUTHENTICATION_METHOD = 'email'  
SOCIALACCOUNT_AUTO_SIGNUP = True  
```  
  
```bash  
python manage.py migrate  
python manage.py createsuperuser  
# Username: admin, Email: admin@example.com, Password: admin123  
```  
  
---  
  
## Part 2: Google OAuth (6 min)  
  
**Get Google Credentials:**  
  
1. Go to: https://console.cloud.google.com/  
2. Create project: "Django OAuth App"  
3. Enable `Google People API` for user data access.  
4. Create OAuth Client ID:  
   - Application type: `Web application`. You may need to first configure the OAuth Consent Screen before creating the Client ID, providing necessary details like app information and scopes.  
   - Authorized redirect URIs: `http://localhost:8000/accounts/google/login/callback/`  
5. Copy Client ID and Client Secret  
  
**Configure in Admin:**  
  
```bash  
python manage.py runserver  
```  
  
1. Visit http://localhost:8000/admin/  
2. Go to "Sites" → Edit "example.com":  
   - Domain: `localhost:8000`  
   - Display name: "OAuth App"  
  
3. Go to "Social applications" → Add:  
   - Provider: Google  
   - Name: Google OAuth  
   - Client ID: (paste yours)  
   - Secret key: (paste yours)  
   - Sites: Select "localhost:8000"  
  
**Create Views `accounts/views.py`:**  
  
```python  
from django.shortcuts import render  
from django.contrib.auth.decorators import login_required  
  
def home(request):  
    return render(request, 'accounts/home.html')  
  
@login_required  
def dashboard(request):  
    return render(request, 'accounts/dashboard.html')  
```  
  
**Create Templates `accounts/templates/accounts/home.html`:**  
  
```html  
<!DOCTYPE html>  
<html>  
<head>  
    <title>Home</title>  
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">  
</head>  
<body>  
    <nav class="navbar navbar-dark bg-dark">  
        <div class="container">  
            <a class="navbar-brand" href="/">OAuth App</a>  
            <div class="navbar-nav ms-auto">  
                {% if user.is_authenticated %}  
                    <a class="nav-link text-white" href="{% url 'dashboard' %}">Dashboard</a>  
                    <a class="nav-link text-white" href="{% url 'account_logout' %}">Logout</a>  
                {% else %}  
                    <a class="nav-link text-white" href="{% url 'account_login' %}">Login</a>  
                {% endif %}  
            </div>  
        </div>  
    </nav>  
  
    <div class="container mt-5 text-center">  
        <h1>Welcome to OAuth App</h1>  
        {% if user.is_authenticated %}  
            <p class="lead">Logged in as: {{ user.email }}</p>  
            <a href="{% url 'dashboard' %}" class="btn btn-primary">Go to Dashboard</a>  
        {% else %}  
            <p class="lead">Login with your Google account</p>  
            <a href="{% url 'account_login' %}" class="btn btn-primary">Login</a>  
        {% endif %}  
    </div>  
</body>  
</html>  
```  
  
**Create `accounts/templates/accounts/dashboard.html`:**  
  
```html  
<!DOCTYPE html>  
<html>  
<head>  
    <title>Dashboard</title>  
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">  
</head>  
<body>  
    <nav class="navbar navbar-dark bg-dark">  
        <div class="container">  
            <a class="navbar-brand" href="/">OAuth App</a>  
            <div class="navbar-nav ms-auto">  
                <a class="nav-link text-white" href="{% url 'account_logout' %}">Logout</a>  
            </div>  
        </div>  
    </nav>  
  
    <div class="container mt-5">  
        <div class="card">  
            <div class="card-header"><h4>Dashboard</h4></div>  
            <div class="card-body">  
                <h5>Welcome, {{ user.email }}!</h5>  
                  
                <hr>  
                  
                <h6>Account Information:</h6>  
                <ul class="list-group">  
                    <li class="list-group-item"><strong>Email:</strong> {{ user.email }}</li>  
                    <li class="list-group-item"><strong>Username:</strong> {{ user.username|default:"Not set" }}</li>  
                    <li class="list-group-item">  
                        <strong>Account Type:</strong>  
                        {% if user.socialaccount_set.all %}  
                            Social Account ({{ user.socialaccount_set.first.provider|title }})  
                        {% else %}  
                            Regular Account  
                        {% endif %}  
                    </li>  
                </ul>  
            </div>  
        </div>  
    </div>  
</body>  
</html>  
```  
  
**Override Login Template `templates/account/login.html`:**  
  
```bash  
mkdir -p templates/account  
```  
  
```html  
{% load socialaccount %}  
<!DOCTYPE html>  
<html>  
<head>  
    <title>Login</title>  
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">  
    <style>  
        .google-btn { background: #4285f4; color: white; }  
    </style>  
</head>  
<body>  
    <div class="container mt-5">  
        <div class="row justify-content-center">  
            <div class="col-md-5">  
                <div class="card">  
                    <div class="card-header"><h4>Login</h4></div>  
                    <div class="card-body">  
                        <a href="{% provider_login_url 'google' %}" class="btn google-btn w-100 mb-3">  
                            <i class="fab fa-google"></i> Continue with Google  
                        </a>  
                          
                        <div class="text-center mb-3"><span class="text-muted">OR</span></div>  
                          
                        <form method="post">  
                            {% csrf_token %}  
                            <div class="mb-3">  
                                <label>Email</label>  
                                <input type="email" name="login" class="form-control" required>  
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
  
---  
  
## Part 3: Security Settings (6 min)  
  
**Update `oauthproject/settings.py` with Security:**  
  
```python  
import os  
  
# Security Settings for Production  
DEBUG = False  # Set to False in production  
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Update with your domain  
  
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-in-production')  
  
# HTTPS/SSL Settings (for production)  
SECURE_SSL_REDIRECT = True  # Force HTTPS  
SESSION_COOKIE_SECURE = True  # HTTPS-only cookies  
CSRF_COOKIE_SECURE = True  # HTTPS-only CSRF cookies  
  
# Security Headers  
SECURE_BROWSER_XSS_FILTER = True  
SECURE_CONTENT_TYPE_NOSNIFF = True  
X_FRAME_OPTIONS = 'DENY'  
  
# HSTS (HTTP Strict Transport Security)  
SECURE_HSTS_SECONDS = 31536000  # 1 year  
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  
SECURE_HSTS_PRELOAD = True  
  
# Session Security  
SESSION_COOKIE_HTTPONLY = True  
SESSION_COOKIE_AGE = 3600  # 1 hour  
  
# CSRF Security  
CSRF_COOKIE_HTTPONLY = True  
CSRF_USE_SESSIONS = True  
  
# Password Validation  
AUTH_PASSWORD_VALIDATORS = [  
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},  
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},  
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},  
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},  
]  
```  
  
**Create Development Settings `oauthproject/settings_dev.py`:**  
  
```python  
from .settings import *  
  
# Override for development  
DEBUG = True  
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']  
  
# Disable HTTPS requirements for local testing  
SECURE_SSL_REDIRECT = False  
SESSION_COOKIE_SECURE = False  
CSRF_COOKIE_SECURE = False  
SECURE_HSTS_SECONDS = 0  
```  
  
**Run with Development Settings:**  
  
```bash  
# For development  
python manage.py runserver --settings=oauthproject.settings_dev  
  
# Or set environment variable  
export DJANGO_SETTINGS_MODULE=oauthproject.settings_dev  
python manage.py runserver  
```  
  
**Create `.env` File (Never commit!):**  
  
```bash  
# .env  
SECRET_KEY=your-super-secret-key-here-change-this  
DEBUG=False  
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com  
GOOGLE_CLIENT_ID=your-client-id  
GOOGLE_CLIENT_SECRET=your-client-secret  
```  
  
**Create `.gitignore`:**  
  
```  
*.pyc  
__pycache__/  
db.sqlite3  
.env  
venv/  
```  
  
**Security Checklist Template `security_checklist.md`:**  
  
```markdown  
## Django Security Checklist  
  
### Production Settings  
- [ ] DEBUG = False  
- [ ] SECRET_KEY in environment variable  
- [ ] ALLOWED_HOSTS configured  
- [ ] SECURE_SSL_REDIRECT = True  
- [ ] SESSION_COOKIE_SECURE = True  
- [ ] CSRF_COOKIE_SECURE = True  
- [ ] SECURE_HSTS_SECONDS set  
- [ ] Strong password validators  
  
### OAuth Security  
- [ ] Client ID/Secret in environment  
- [ ] Redirect URIs whitelisted  
- [ ] HTTPS enabled  
- [ ] Token expiry configured  
  
### General Security  
- [ ] Admin URL changed from /admin/  
- [ ] Regular Django updates  
- [ ] Database backups  
- [ ] SSL certificate installed  
- [ ] Firewall configured  
```  
  
**Configure URLs:**  
  
```python  
# accounts/urls.py  
from django.urls import path  
from . import views  
  
urlpatterns = [  
    path('', views.home, name='home'),  
    path('dashboard/', views.dashboard, name='dashboard'),  
]  
  
# oauthproject/urls.py  
from django.contrib import admin  
from django.urls import path, include  
  
urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('accounts/', include('allauth.urls')),  
    path('', include('accounts.urls')),  
]  
```  
  
**Update `oauthproject/settings.py` Templates:**  
  
```python  
TEMPLATES = [  
    {  
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  
        'DIRS': [BASE_DIR / 'templates'],  
        'APP_DIRS': True,  
        'OPTIONS': {  
            'context_processors': [  
                'django.template.context_processors.debug',  
                'django.template.context_processors.request',  
                'django.contrib.auth.context_processors.auth',  
                'django.contrib.messages.context_processors.messages',  
            ],  
        },  
    },  
]  
```  
  
---  
  
## Quick Test  
  
```bash  
python manage.py runserver --settings=oauthproject.settings_dev  
```  
  
**Test OAuth:**  
  
1. Visit http://localhost:8000/accounts/login/  
2. Click "Continue with Google"  
3. Select your Google account  
4. Authorize app  
5. Redirected to dashboard  
6. Check: Email populated from Google!  
  
**Test Security:**  
  
```bash  
# Check security issues  
python manage.py check --deploy  
  
# Expected warnings in development (OK)  
# Should show no errors in production  
```  
  
---  
  
## What You Learned  
  
✅ **Django OAuth:**  
- django-allauth integration  
- Google OAuth 2.0 flow  
- Social account linking  
- No password needed!  
  
✅ **Security:**  
- DEBUG = False in production  
- HTTPS/SSL configuration  
- Secure cookies  
- HSTS headers  
- Strong password validation  
- Environment variables  
  
✅ **Best Practices:**  
- Separate dev/prod settings  
- .env for secrets  
- .gitignore for sensitive files  
- Security checklist  
  
---  
  
## Quick Quiz  
  
**Q1:** Why should DEBUG be False in production?  
  
<details>  
<summary>Answer</summary>  
DEBUG=True exposes sensitive information (settings, queries, stack traces) to users. Security risk!  
</details>  
  
**Q2:** What does SECURE_SSL_REDIRECT do?  
  
<details>  
<summary>Answer</summary>  
Forces all HTTP requests to redirect to HTTPS. Ensures encrypted connections.  
</details>  
  
**Q3:** Where should SECRET_KEY be stored?  
  
<details>  
<summary>Answer</summary>  
In environment variable, never in code. Use .env file (excluded from git).  
</details>  
  
---  
  
**Time Taken:** 15 minutes    
**Security Score:** A+ (with all settings)    
**Lines of Code:** ~150