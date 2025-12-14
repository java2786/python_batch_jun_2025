# Core Architecture & Flow for Each Mini-App  
  
## Mini-App 1: Photo Upload with Email  
### Core Parts:  
1. Settings Configuration:  
```python  
MEDIA_URL = '/media/'  
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  
```  
  
2. Model with ImageField:  
```python  
class Profile(models.Model):  
    photo = models.ImageField(upload_to='photos/')  # Core: File storage  
```  
  
3. Form Validation:  
```python  
def clean_photo(self):  
    # Validate size (max 2MB)  
    # Validate extension (.jpg, .png)  
```  
  
4. View Flow:  
```python  
upload_photo(request)  
  ↓  
Save photo to media/photos/  
  ↓  
send_upload_email(user, profile)  
  ↓  
EmailMessage.attach_file(photo.path)  # Core: Attach file  
```  
  
### Data Flow:  
```  
User selects photo  
  ↓  
Form validates (size, type)  
  ↓  
File saved to: media/photos/filename.jpg  
  ↓  
Email sent with attachment  
  ↓  
Terminal shows email output  
```  
  
---  
  
## Mini-App 2: Product Filter with Cache  
### Core Parts:  
1. Cache Configuration:  
```python  
CACHES = {  
    'default': {  
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',  
        'TIMEOUT': 300,  # 5 minutes  
    }  
}  
```  
  
2. ORM Query Optimization:  
```python  
Product.objects.select_related('category')  # JOIN in 1 query  
Product.objects.filter(Q(name__icontains=keyword))  # OR conditions  
Category.objects.annotate(total=Count('products'))  # Aggregation  
```  
  
3. Caching Logic:  
```python  
cache_key = f'products_{category}_{min_price}_{max_price}'  
products = cache.get(cache_key)  
  
if products is None:  
    products = Product.objects.all()  # Database query  
    cache.set(cache_key, products, 300)  # Store for 5 min  
```  
  
### Performance Flow:  
```  
First Request:  
  ↓  
cache.get() → MISS  
  ↓  
Query database (15ms)  
  ↓  
cache.set()  
  ↓  
Return data  
  
Second Request (same filters):  
  ↓  
cache.get() → HIT  
  ↓  
Return from memory (0.5ms)  # 30x faster!  
```  
  
---  
  
## Mini-App 3: Shopping Cart  
### Core Parts:  
1. Session Configuration:  
```python  
SESSION_COOKIE_AGE = 86400  # 24 hours  
SESSION_SAVE_EVERY_REQUEST = True  
```  
  
2. Cart Class (Session Storage):  
```python  
class Cart:  
    def __init__(self, request):  
        self.session = request.session  
        self.cart = self.session.get('cart', {})  
      
    def add(self, product_id, quantity):  
        self.cart[product_id] = {'quantity': quantity}  
        self.session.modified = True  # Core: Mark as changed  
```  
  
3. Cookie for Theme:  
```python  
response.set_cookie('theme', 'dark', max_age=365*24*60*60)  # 1 year  
theme = request.COOKIES.get('theme', 'light')  
```  
  
### Data Flow:  
```  
Sessions (Server-side):  
Cart data → request.session['cart'] = {'1': {'quantity': 2}}  
  ↓  
Stored in database (django_session table)  
  ↓  
Only session ID in cookie: sessionid=abc123  
  
Cookies (Client-side):  
Theme preference → response.set_cookie('theme', 'dark')  
  ↓  
Stored in browser  
  ↓  
Sent with every request: Cookie: theme=dark  
```  
  
---  
  
## Mini-App 4: Task Manager with CBV & Tests  
### Core Parts:  
1. Class Based Views:  
```python  
# ListView - Display all  
class TaskListView(ListView):  
    model = Task  
      
# CreateView - Create new  
class TaskCreateView(CreateView):  
    model = Task  
    fields = ['title', 'description']  
      
    def form_valid(self, form):  
        form.instance.user = self.request.user  # Core: Auto-set user  
```  
  
2. Permissions with Mixins:  
```python  
class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  
    def test_func(self):  
        return self.request.user == self.get_object().user  # Core: Owner only  
```  
  
3. Test Structure:  
```python  
class TaskViewTest(TestCase):  
    def setUp(self):  
        self.user = User.objects.create_user(...)  # Create test data  
        self.task = Task.objects.create(...)  
      
    def test_task_create(self):  
        response = self.client.post(...)  
        self.assertEqual(response.status_code, 302)  # Check redirect  
        self.assertEqual(Task.objects.count(), 2)  # Verify created  
```  
  
### CBV Flow:  
```  
URL: /tasks/create/  
  ↓  
TaskCreateView.as_view()  
  ↓  
GET: Display form  
  ↓  
POST: form_valid() → Save + Set user  
  ↓  
Redirect to success_url  
```  
  
---  
  
## Mini-App 5: OAuth & Security  
### Core Parts:  
1. OAuth Configuration:  
```python  
INSTALLED_APPS = [  
    'allauth',  
    'allauth.socialaccount',  
    'allauth.socialaccount.providers.google',  # Core: Enable Google  
]  
  
AUTHENTICATION_BACKENDS = [  
    'allauth.account.auth_backends.AuthenticationBackend',  # Core: OAuth backend  
]  
```  
  
2. Security Settings:  
```python  
# Production Security  
DEBUG = False  
SECRET_KEY = os.environ.get('SECRET_KEY')  # Core: Environment variable  
SECURE_SSL_REDIRECT = True  # Core: Force HTTPS  
SESSION_COOKIE_SECURE = True  # Core: HTTPS-only cookies  
CSRF_COOKIE_SECURE = True  
```  
  
**3. Google Provider in Admin:**  
```  
Social applications:  
  - Provider: Google  
  - Client ID: from Google Console  
  - Secret key: from Google Console  
  - Sites: localhost:8000  
```  
  
### OAuth Flow:  
```  
User clicks "Login with Google"  
  ↓  
Redirect to Google: accounts.google.com/o/oauth2/auth  
  ↓  
User authorizes  
  ↓  
Google redirects: /accounts/google/login/callback/?code=abc123  
  ↓  
django-allauth exchanges code for token  
  ↓  
Fetch user data (email, name)  
  ↓  
Create/login user in Django  
  ↓  
Redirect to dashboard  
```  
  
---  
  
## Mini-App 6: REST API  
### Core Parts:  
1. DRF Configuration:  
```python  
INSTALLED_APPS = [  
    'rest_framework',  
    'rest_framework.authtoken',  # Core: Token auth  
]  
  
REST_FRAMEWORK = {  
    'DEFAULT_AUTHENTICATION_CLASSES': [  
        'rest_framework.authentication.TokenAuthentication',  # Core  
    ],  
    'DEFAULT_PERMISSION_CLASSES': [  
        'rest_framework.permissions.IsAuthenticated',  # Core: Require auth  
    ],  
}  
```  
  
2. Serializer (Model ↔ JSON):  
```python  
class NoteSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Note  
        fields = ['id', 'title', 'content']  # Core: Which fields to expose  
```  
  
3. ViewSet (Auto CRUD):  
```python  
class NoteViewSet(viewsets.ModelViewSet):  
    serializer_class = NoteSerializer  
      
    def get_queryset(self):  
        return Note.objects.filter(user=self.request.user)  # Core: User's notes only  
      
    def perform_create(self, serializer):  
        serializer.save(user=self.request.user)  # Core: Auto-set user  
```  
  
4. Token Authentication:  
```python  
# Register/Login returns token  
Token.objects.get_or_create(user=user)  
return Response({'token': token.key})  
  
# Client sends in header  
Authorization: Token abc123xyz789  
```  
  
### API Request Flow:  
```  
POST /api/auth/login/  
  ↓  
Authenticate user  
  ↓  
Generate/get token  
  ↓  
Return: {"token": "abc123"}  
  
POST /api/notes/  
Headers: Authorization: Token abc123  
  ↓  
Validate token  
  ↓  
Deserialize JSON → Model  
  ↓  
Save to database  
  ↓  
Serialize Model → JSON  
  ↓  
Return: {"id": 1, "title": "..."}  
```  
  
---  
  
Quick Reference Table  
  
| App | Core Component | Key Flow |  
|-----|----------------|----------|  
| 1 | ImageField + EmailMessage.attach_file() | Upload → Validate → Save → Email |  
| 2 | cache.get/set() + select_related() | Check cache → Query DB → Store cache |  
| 3 | request.session['cart'] + set_cookie() | Session (cart data) + Cookie (theme) |  
| 4 | CreateView + UserPassesTestMixin | CBV auto-handles forms + Tests verify |  
| 5 | allauth + SECURE_SSL_REDIRECT | OAuth provider + Security settings |  
| 6 | ModelViewSet + TokenAuthentication | Serializer ↔ JSON + Token in header |  
  
This gives anyone a quick understanding of the essential parts and data flow before diving into the full code! 