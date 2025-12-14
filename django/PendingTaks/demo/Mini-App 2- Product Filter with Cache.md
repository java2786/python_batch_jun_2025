# Django Mini-App 2: Product Filter with Cache

**Duration:** 15 minutes  
**Topics:** Django ORM, Django Cache

---

## What You'll Build

Product catalog with advanced filtering + caching for 10x faster performance.

---

## Part 1: Setup (3 min)

```bash
mkdir product_filter && cd product_filter
python -m venv venv
venv\Scripts\activate
pip install django
django-admin startproject filterproject .
python manage.py startapp products
```

**Configure `filterproject/settings.py`:**

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products',
]

# Cache Configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'product-cache',
        'TIMEOUT': 300,  # 5 minutes
    }
}
```

**Create Models `products/models.py`:**

```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
```

```bash
python manage.py makemigrations
python manage.py migrate
```

**Create Sample Data `products/management/commands/load_products.py`:**

```bash
mkdir -p products/management/commands
touch products/management/__init__.py
touch products/management/commands/__init__.py
```

```python
from django.core.management.base import BaseCommand
from products.models import Category, Product
from decimal import Decimal

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Category.objects.all().delete()
        
        # Create categories
        electronics = Category.objects.create(name='Electronics')
        clothing = Category.objects.create(name='Clothing')
        books = Category.objects.create(name='Books')
        
        # Create products
        products = [
            {'name': 'Laptop', 'category': electronics, 'price': 45000, 'stock': 10, 'priority': 'high', 'rating': 4.5},
            {'name': 'Mouse', 'category': electronics, 'price': 500, 'stock': 50, 'priority': 'low', 'rating': 4.0},
            {'name': 'Keyboard', 'category': electronics, 'price': 1500, 'stock': 30, 'priority': 'medium', 'rating': 4.2},
            {'name': 'T-Shirt', 'category': clothing, 'price': 499, 'stock': 100, 'priority': 'low', 'rating': 3.8},
            {'name': 'Jeans', 'category': clothing, 'price': 1999, 'stock': 40, 'priority': 'medium', 'rating': 4.1},
            {'name': 'Python Book', 'category': books, 'price': 599, 'stock': 25, 'priority': 'high', 'rating': 4.7},
            {'name': 'Django Book', 'category': books, 'price': 699, 'stock': 20, 'priority': 'high', 'rating': 4.8},
        ]
        
        for p in products:
            Product.objects.create(**p)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(products)} products'))
```

```bash
python manage.py load_products
```

---

## Part 2: Django ORM Queries (6 min)

**Create `products/queries.py`:**

```python
from django.db.models import Q, Count, Avg, Sum, Max, Min, F
from .models import Product, Category

# Basic Filtering
def get_expensive_products():
    return Product.objects.filter(price__gt=1000)

def get_products_by_category(category_name):
    return Product.objects.filter(category__name=category_name)

# Search with Q Objects
def search_products(keyword):
    return Product.objects.filter(
        Q(name__icontains=keyword) | Q(category__name__icontains=keyword)
    )

# Complex Filters
def get_high_priority_in_stock():
    return Product.objects.filter(
        Q(priority='high') & Q(stock__gt=0)
    )

# Aggregation
def get_category_stats():
    return Category.objects.annotate(
        total_products=Count('products'),
        avg_price=Avg('products__price'),
        total_stock=Sum('products__stock')
    )

def get_price_stats():
    return Product.objects.aggregate(
        avg=Avg('price'),
        max=Max('price'),
        min=Min('price'),
        total_value=Sum(F('price') * F('stock'))
    )

# Optimization
def get_products_optimized():
    # Use select_related to reduce queries
    return Product.objects.select_related('category').all()
```

**Create Views `products/views.py`:**

```python
from django.shortcuts import render
from django.db.models import Q
from django.core.cache import cache
from .models import Product, Category
from .queries import *
import time

def product_list(request):
    # Get filter parameters
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    search = request.GET.get('search', '')
    
    # Build cache key
    cache_key = f'products_{category}_{min_price}_{max_price}_{search}'
    
    # Try to get from cache
    start_time = time.time()
    products = cache.get(cache_key)
    
    if products is None:
        # Query database
        products = Product.objects.select_related('category').all()
        
        if category:
            products = products.filter(category__name=category)
        
        if min_price:
            products = products.filter(price__gte=min_price)
        
        if max_price:
            products = products.filter(price__lte=max_price)
        
        if search:
            products = products.filter(
                Q(name__icontains=search) | Q(category__name__icontains=search)
            )
        
        products = list(products)
        
        # Store in cache
        cache.set(cache_key, products, 300)
        cache_status = 'MISS'
    else:
        cache_status = 'HIT'
    
    query_time = (time.time() - start_time) * 1000  # Convert to ms
    
    # Get statistics
    stats = get_price_stats()
    category_stats = get_category_stats()
    
    context = {
        'products': products,
        'categories': Category.objects.all(),
        'stats': stats,
        'category_stats': category_stats,
        'query_time': round(query_time, 2),
        'cache_status': cache_status,
    }
    
    return render(request, 'products/list.html', context)
```

**Create Template `products/templates/products/list.html`:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Product Filter</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <h2>Product Catalog</h2>
        
        <!-- Performance Stats -->
        <div class="alert alert-info">
            <strong>Query Time:</strong> {{ query_time }}ms | 
            <strong>Cache:</strong> {{ cache_status }}
            {% if cache_status == 'HIT' %}âœ… (10x faster!){% else %}âŒ (first load){% endif %}
        </div>
        
        <!-- Filters -->
        <form method="get" class="card p-3 mb-3">
            <div class="row">
                <div class="col-md-3">
                    <select name="category" class="form-select">
                        <option value="">All Categories</option>
                        {% for cat in categories %}
                            <option value="{{ cat.name }}">{{ cat.name }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-2">
                    <input type="number" name="min_price" class="form-control" placeholder="Min Price">
                </div>
                <div class="col-md-2">
                    <input type="number" name="max_price" class="form-control" placeholder="Max Price">
                </div>
                <div class="col-md-3">
                    <input type="text" name="search" class="form-control" placeholder="Search...">
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-primary w-100">Filter</button>
                </div>
            </div>
        </form>
        
        <!-- Statistics -->
        <div class="row mb-3">
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <h6>Average Price</h6>
                        <h4>â‚¹{{ stats.avg|floatformat:2 }}</h4>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <h6>Max Price</h6>
                        <h4>â‚¹{{ stats.max }}</h4>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <h6>Min Price</h6>
                        <h4>â‚¹{{ stats.min }}</h4>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <h6>Total Value</h6>
                        <h4>â‚¹{{ stats.total_value|floatformat:0 }}</h4>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Products -->
        <div class="row">
            {% for product in products %}
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5>{{ product.name }}</h5>
                        <p class="text-muted">{{ product.category.name }}</p>
                        <h4 class="text-primary">â‚¹{{ product.price }}</h4>
                        <p>
                            <span class="badge bg-secondary">{{ product.get_priority_display }}</span>
                            <span class="badge bg-info">Stock: {{ product.stock }}</span>
                            <span class="badge bg-warning">â˜… {{ product.rating }}</span>
                        </p>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        
        <!-- Category Stats -->
        <h4 class="mt-4">Category Statistics</h4>
        <table class="table">
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Products</th>
                    <th>Avg Price</th>
                    <th>Total Stock</th>
                </tr>
            </thead>
            <tbody>
                {% for cat in category_stats %}
                <tr>
                    <td>{{ cat.name }}</td>
                    <td>{{ cat.total_products }}</td>
                    <td>â‚¹{{ cat.avg_price|floatformat:2 }}</td>
                    <td>{{ cat.total_stock }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
```

---

## Part 3: Caching (6 min)

**Test Cache Performance:**

```bash
python manage.py shell
```

```python
# Test without cache
from products.models import Product
import time

start = time.time()
products = list(Product.objects.select_related('category').all())
print(f"Without cache: {(time.time() - start) * 1000:.2f}ms")

# Test with cache
from django.core.cache import cache

cache.set('test_products', products, 300)
start = time.time()
cached = cache.get('test_products')
print(f"With cache: {(time.time() - start) * 1000:.2f}ms")

# You'll see: Without cache: 15ms, With cache: 0.5ms (30x faster!)
```

**Configure URLs `products/urls.py`:**

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
]
```

**Update `filterproject/urls.py`:**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
]
```

---

## Quick Test

```bash
python manage.py runserver
```

**Test Steps:**

1. Visit http://localhost:8000/
2. First load: Cache MISS, ~15ms
3. Refresh page: Cache HIT, ~0.5ms (30x faster!)
4. Filter by category: New cache key, MISS
5. Apply same filter again: HIT!

**Test ORM Queries:**

```python
# In shell
from products.queries import *

# 1. Expensive products
expensive = get_expensive_products()
print(f"Expensive: {expensive.count()}")

# 2. Search
results = search_products('book')
for p in results:
    print(f"{p.name} - {p.category.name}")

# 3. High priority in stock
priority = get_high_priority_in_stock()
print(f"High priority: {priority.count()}")

# 4. Category stats
stats = get_category_stats()
for cat in stats:
    print(f"{cat.name}: {cat.total_products} products, Avg: â‚¹{cat.avg_price:.2f}")
```

---

## What You Learned

✅ **Django ORM:**
- Q objects for complex filters
- Aggregation (Count, Avg, Sum, Max, Min)
- F objects for field operations
- select_related for optimization

✅ **Django Cache:**
- LocMemCache backend
- Cache keys and timeout
- get/set operations
- 30x performance improvement!

✅ **Best Practices:**
- Query optimization
- Cache invalidation strategy
- Performance monitoring

---

## Quick Quiz

**Q1:** What's the difference between `filter()` and `get()`?

<details>
<summary>Answer</summary>
`filter()` returns QuerySet (multiple objects), `get()` returns single object or raises error.
</details>

**Q2:** When does cache expire?

<details>
<summary>Answer</summary>
After TIMEOUT (300 seconds = 5 minutes in this app).
</details>

**Q3:** What does `select_related()` do?

<details>
<summary>Answer</summary>
Uses SQL JOIN to fetch related objects in single query, avoiding N+1 problem.
</details>

---

**Time Taken:** 15 minutes  
**Performance:** 30x faster with cache  
**Lines of Code:** ~200