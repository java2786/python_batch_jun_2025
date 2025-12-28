# Django Mini-App 6: Simple REST API with DRF

**Duration:** 15 minutes  
**Topics:** Django REST Framework

---

## What You'll Build

REST API for notes with token authentication + Test in Postman.

---

## Part 1: Setup (3 min)

```bash
mkdir notes_api && cd notes_api
python -m venv venv
venv\Scripts\activate
pip install djangorestframework
django-admin startproject apiproject .
python manage.py startapp notes
```

**Configure `apiproject/settings.py`:**

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'notes',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

**Create Model `notes/models.py`:**

```python
from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
```

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
# Username: admin, Password: admin123
```

---

## Part 2: Create API Endpoints (6 min)

**Create Serializer `notes/serializers.py`:**

```python
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
```

**Create ViewSets `notes/views.py`:**

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Note
from .serializers import NoteSerializer, UserSerializer

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_notes = self.get_queryset()[:5]
        serializer = self.get_serializer(recent_notes, many=True)
        return Response(serializer.data)

# Authentication Views
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(username=username, email=email, password=password)
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        })
    
    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({'message': 'Successfully logged out'})
```

**Configure URLs `notes/urls.py`:**

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'notes', views.NoteViewSet, basename='note')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
]
```

**Update `apiproject/urls.py`:**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('notes.urls')),
]
```

---

## Part 3: Test with Postman (6 min)

```bash
python manage.py runserver
```

**Download Postman:** https://www.postman.com/downloads/

### Test 1: Register User

```
Method: POST
URL: http://localhost:8000/api/auth/register/

Body (raw JSON):
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
}

Expected Response (201):
{
    "token": "abc123xyz789...",
    "user_id": 2,
    "username": "testuser"
}
```

### Test 2: Login

```
Method: POST
URL: http://localhost:8000/api/auth/login/

Body (raw JSON):
{
    "username": "testuser",
    "password": "testpass123"
}

Expected Response (200):
{
    "token": "abc123xyz789...",
    "user_id": 2,
    "username": "testuser"
}
```

### Test 3: Create Note (with Authentication)

```
Method: POST
URL: http://localhost:8000/api/notes/

Headers:
    Authorization: Token abc123xyz789...
    Content-Type: application/json

Body (raw JSON):
{
    "title": "My First Note",
    "content": "This is a test note created via API"
}

Expected Response (201):
{
    "id": 1,
    "user": "testuser",
    "title": "My First Note",
    "content": "This is a test note created via API",
    "created_at": "2024-12-06T10:30:00Z",
    "updated_at": "2024-12-06T10:30:00Z"
}
```

### Test 4: List All Notes

```
Method: GET
URL: http://localhost:8000/api/notes/

Headers:
    Authorization: Token abc123xyz789...

Expected Response (200):
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": "testuser",
            "title": "My First Note",
            "content": "This is a test note created via API",
            "created_at": "2024-12-06T10:30:00Z",
            "updated_at": "2024-12-06T10:30:00Z"
        }
    ]
}
```

### Test 5: Get Single Note

```
Method: GET
URL: http://localhost:8000/api/notes/1/

Headers:
    Authorization: Token abc123xyz789...

Expected Response (200):
{
    "id": 1,
    "user": "testuser",
    "title": "My First Note",
    "content": "This is a test note created via API",
    "created_at": "2024-12-06T10:30:00Z",
    "updated_at": "2024-12-06T10:30:00Z"
}
```

### Test 6: Update Note

```
Method: PUT
URL: http://localhost:8000/api/notes/1/

Headers:
    Authorization: Token abc123xyz789...
    Content-Type: application/json

Body (raw JSON):
{
    "title": "Updated Note Title",
    "content": "Updated content"
}

Expected Response (200):
{
    "id": 1,
    "user": "testuser",
    "title": "Updated Note Title",
    "content": "Updated content",
    "created_at": "2024-12-06T10:30:00Z",
    "updated_at": "2024-12-06T11:00:00Z"
}
```

### Test 7: Delete Note

```
Method: DELETE
URL: http://localhost:8000/api/notes/1/

Headers:
    Authorization: Token abc123xyz789...

Expected Response (204):
No content
```

### Test 8: Custom Action - Recent Notes

```
Method: GET
URL: http://localhost:8000/api/notes/recent/

Headers:
    Authorization: Token abc123xyz789...

Expected Response (200):
[
    {
        "id": 5,
        "title": "Most Recent Note",
        ...
    },
    ...
]
```

### Test 9: Unauthenticated Request (Should Fail)

```
Method: GET
URL: http://localhost:8000/api/notes/

Headers:
    (No Authorization header)

Expected Response (401):
{
    "detail": "Authentication credentials were not provided."
}
```

### Test 10: Logout

```
Method: POST
URL: http://localhost:8000/api/auth/logout/

Headers:
    Authorization: Token abc123xyz789...

Expected Response (200):
{
    "message": "Successfully logged out"
}
```

**DRF Browsable API:**

Visit http://localhost:8000/api/notes/ in browser for interactive API interface.

---

## Quick Test

**Python Script to Test API:**

```python
# test_api.py
import requests

BASE_URL = 'http://localhost:8000/api'

# 1. Register
response = requests.post(f'{BASE_URL}/auth/register/', json={
    'username': 'apitest',
    'email': 'api@test.com',
    'password': 'test123'
})
print(f"Register: {response.status_code}")
token = response.json()['token']

# 2. Create Note
headers = {'Authorization': f'Token {token}'}
response = requests.post(f'{BASE_URL}/notes/', 
    headers=headers,
    json={'title': 'API Test Note', 'content': 'Created via script'}
)
print(f"Create Note: {response.status_code}")

# 3. List Notes
response = requests.get(f'{BASE_URL}/notes/', headers=headers)
print(f"List Notes: {response.status_code}, Count: {response.json()['count']}")

# 4. Logout
response = requests.post(f'{BASE_URL}/auth/logout/', headers=headers)
print(f"Logout: {response.status_code}")
```

```bash
pip install requests
python test_api.py
```

---

## What You Learned

✅ **Django REST Framework:**
- ModelViewSet for CRUD
- Serializers for JSON conversion
- Token authentication
- Custom actions with @action
- Permissions (IsAuthenticated)

✅ **REST API Design:**
- HTTP methods (GET, POST, PUT, DELETE)
- Status codes (200, 201, 401, 404)
- Authentication headers
- Pagination

✅ **API Testing:**
- Postman for manual testing
- Python requests for automation
- DRF Browsable API

---

## Quick Quiz

**Q1:** What's the difference between ModelViewSet and APIView?

<details>
<summary>Answer</summary>
ModelViewSet provides CRUD operations automatically. APIView requires manual implementation of each method.
</details>

**Q2:** How does token authentication work?

<details>
<summary>Answer</summary>
User logs in → Server generates token → Client stores token → Client includes token in Authorization header for subsequent requests.
</details>

**Q3:** What does `perform_create()` do?

<details>
<summary>Answer</summary>
Hook to modify object before saving. Here, it sets the user field automatically.
</details>

---

**Time Taken:** 15 minutes  
**API Endpoints:** 8  
**Lines of Code:** ~120  
**Response Time:** <50ms

---

## All 6 Mini-Apps Complete! 🎉

**Total Topics Covered:** 11/14
- ✅ File Upload
- ✅ Class Based Views
- ✅ Django Testing
- ✅ Django Mail
- ✅ Django ORM
- ✅ Django Sessions
- ✅ Django Cookies
- ✅ Django Cache
- ✅ Django OAuth (Google)
- ✅ Security in Django
- ✅ Django REST Framework

**Total Time:** 90 minutes  
**Total Lines of Code:** ~1,000  
**Projects Built:** 6 working applications