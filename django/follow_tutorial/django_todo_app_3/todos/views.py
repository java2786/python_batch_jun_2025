from django.shortcuts import render, redirect, get_object_or_404  
from django.contrib.auth import login, logout, authenticate  
from django.contrib.auth.decorators import login_required  
from django.contrib.auth.models import User  
from django.contrib import messages  
from .models import Todo  
from django.db.models import Q 
from django.contrib.auth import update_session_auth_hash  
  
# ========== TODO VIEWS (UPDATE EXISTING) ==========  
  
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