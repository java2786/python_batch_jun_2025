# Django Mini-App 3: Shopping Cart with Sessions & Cookies

**Duration:** 15 minutes  
**Topics:** Django Sessions, Django Cookies

---

## What You'll Build

Shopping cart (sessions) + Theme preference (cookies).

---

## Part 1: Setup (3 min)

```bash
mkdir shopping_cart && cd shopping_cart
python -m venv venv
venv\Scripts\activate
pip install django
django-admin startproject cartproject .
python manage.py startapp shop
```

**Configure `cartproject/settings.py`:**

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
]

# Session Configuration
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = True
```

**Create Model `shop/models.py`:**

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    
    def __str__(self):
        return self.name
```

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
# Username: admin, Password: admin123
```

**Add Sample Products in Admin:**

```bash
python manage.py shell
```

```python
from shop.models import Product

products = [
    {'name': 'Laptop', 'price': 45000, 'description': 'High performance laptop'},
    {'name': 'Mouse', 'price': 500, 'description': 'Wireless mouse'},
    {'name': 'Keyboard', 'price': 1500, 'description': 'Mechanical keyboard'},
]

for p in products:
    Product.objects.create(**p)

print("Sample products created!")
```

---

## Part 2: Sessions - Shopping Cart (6 min)

**Create Cart Class `shop/cart.py`:**

```python
from decimal import Decimal
from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
    
    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
        
        self.cart[product_id]['quantity'] += quantity
        self.save()
    
    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def save(self):
        self.session.modified = True
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['total_price'] = item['product'].price * item['quantity']
            yield item
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(item['product'].price * item['quantity'] for item in self)
    
    def clear(self):
        del self.session['cart']
        self.save()
```

**Create Views `shop/views.py`:**

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Product
from .cart import Cart

def product_list(request):
    products = Product.objects.all()
    cart = Cart(request)
    
    # Get theme from cookie
    theme = request.COOKIES.get('theme', 'light')
    
    return render(request, 'shop/product_list.html', {
        'products': products,
        'cart': cart,
        'theme': theme,
    })

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart.add(product_id=product.id, quantity=quantity)
    messages.success(request, f'{product.name} added to cart!')
    
    return redirect('product_list')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    messages.success(request, 'Item removed from cart!')
    
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    theme = request.COOKIES.get('theme', 'light')
    
    return render(request, 'shop/cart.html', {
        'cart': cart,
        'theme': theme,
    })

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, 'Cart cleared!')
    
    return redirect('cart_detail')
```

---

## Part 3: Cookies - Theme Preference (6 min)

**Add Theme View in `shop/views.py`:**

```python
def set_theme(request):
    theme = request.GET.get('theme', 'light')
    response = redirect(request.META.get('HTTP_REFERER', 'product_list'))
    
    # Set cookie for 1 year
    response.set_cookie('theme', theme, max_age=365*24*60*60)
    
    messages.success(request, f'Theme changed to {theme}!')
    return response
```

**Create Templates `shop/templates/shop/product_list.html`:**

```html
<!DOCTYPE html>
<html data-bs-theme="{{ theme }}">
<head>
    <title>Products</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container">
            <a class="navbar-brand" href="{% url 'product_list' %}">Shop</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="{% url 'cart_detail' %}">
                    Cart ({{ cart|length }})
                </a>
                <div class="dropdown">
                    <button class="btn btn-sm btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown">
                        Theme: {{ theme|title }}
                    </button>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="{% url 'set_theme' %}?theme=light">Light</a></li>
                        <li><a class="dropdown-item" href="{% url 'set_theme' %}?theme=dark">Dark</a></li>
                    </ul>
                </div>
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

        <h2>Products</h2>
        
        <div class="row">
            {% for product in products %}
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ product.name }}</h5>
                        <p class="card-text">{{ product.description }}</p>
                        <h4 class="text-primary">â‚¹{{ product.price }}</h4>
                        <form method="post" action="{% url 'cart_add' product.id %}">
                            {% csrf_token %}
                            <div class="input-group mb-2">
                                <input type="number" name="quantity" value="1" min="1" class="form-control" style="max-width: 80px;">
                                <button type="submit" class="btn btn-primary">Add to Cart</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

**Create Cart Template `shop/templates/shop/cart.html`:**

```html
<!DOCTYPE html>
<html data-bs-theme="{{ theme }}">
<head>
    <title>Shopping Cart</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container">
            <a class="navbar-brand" href="{% url 'product_list' %}">Shop</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="{% url 'cart_detail' %}">Cart ({{ cart|length }})</a>
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

        <h2>Shopping Cart</h2>

        {% if cart %}
        <div class="card">
            <div class="card-body">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Price</th>
                            <th>Quantity</th>
                            <th>Total</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in cart %}
                        <tr>
                            <td>{{ item.product.name }}</td>
                            <td>â‚¹{{ item.product.price }}</td>
                            <td>{{ item.quantity }}</td>
                            <td>â‚¹{{ item.total_price }}</td>
                            <td>
                                <form method="post" action="{% url 'cart_remove' item.product.id %}" class="d-inline">
                                    {% csrf_token %}
                                    <button type="submit" class="btn btn-sm btn-danger">Remove</button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                    <tfoot>
                        <tr>
                            <td colspan="3"><strong>Total:</strong></td>
                            <td colspan="2"><strong>â‚¹{{ cart.get_total_price }}</strong></td>
                        </tr>
                    </tfoot>
                </table>

                <div class="d-flex justify-content-between">
                    <a href="{% url 'product_list' %}" class="btn btn-secondary">Continue Shopping</a>
                    <a href="{% url 'cart_clear' %}" class="btn btn-warning">Clear Cart</a>
                    <button class="btn btn-success">Checkout</button>
                </div>
            </div>
        </div>
        {% else %}
        <div class="alert alert-info">
            Your cart is empty! <a href="{% url 'product_list' %}">Start shopping</a>
        </div>
        {% endif %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

**Configure URLs `shop/urls.py`:**

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),
    path('set-theme/', views.set_theme, name='set_theme'),
]
```

**Update `cartproject/urls.py`:**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
]
```

---

## Quick Test

```bash
python manage.py runserver
```

**Test Sessions (Cart):**

1. Visit http://localhost:8000/
2. Add "Laptop" (quantity: 1) → Cart (1)
3. Add "Mouse" (quantity: 2) → Cart (3)
4. Go to Cart → See all items
5. Close browser → Reopen → Cart persists (24 hours)!

**Test Cookies (Theme):**

1. Click "Theme: Light" dropdown → Select "Dark"
2. Page reloads in dark mode
3. Navigate between pages → Theme persists
4. Close browser → Reopen → Theme still dark!

**Verify in Browser DevTools:**

```
Application → Cookies → localhost:8000
- theme: dark (expires in 1 year)

Application → Session Storage → sessionid
- Session contains cart data
```

---

## What You Learned

✅ **Django Sessions:**
- Store cart data server-side
- Session expiry (24 hours)
- `session.modified = True` for nested data
- Persist across browser sessions

✅ **Django Cookies:**
- Store preferences client-side
- Set cookie with `response.set_cookie()`
- Get cookie with `request.COOKIES.get()`
- Max age (1 year for theme)

✅ **Best Practices:**
- Sessions for sensitive data (cart)
- Cookies for preferences (theme)
- User feedback with messages

---

## Quick Quiz

**Q1:** Where is session data stored?

<details>
<summary>Answer</summary>
Server-side (database by default). Only session ID stored in cookie.
</details>

**Q2:** What's the difference between sessions and cookies?

<details>
<summary>Answer</summary>
Sessions: Server-side, secure, larger data. Cookies: Client-side, less secure, small data (4KB limit).
</details>

**Q3:** Why use `session.modified = True`?

<details>
<summary>Answer</summary>
Django doesn't detect changes in nested data (dict, list). This forces session to save.
</details>

---

**Time Taken:** 15 minutes  
**Session Size:** ~500 bytes  
**Cookie Size:** ~20 bytes  
**Lines of Code:** ~180