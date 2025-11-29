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