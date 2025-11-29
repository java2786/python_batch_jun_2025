from django.shortcuts import render, redirect, get_object_or_404  
from .models import Todo  
  
# Show all todos  
def todo_list(request):  
    todos = Todo.objects.all()  
    return render(request, 'todos/todo_list.html', {'todos': todos})  
  
# Create new todo  
def todo_create(request):  
    if request.method == 'POST':  
        title = request.POST.get('title')  
        description = request.POST.get('description')  
          
        Todo.objects.create(  
            title=title,  
            description=description  
        )  
        return redirect('todo_list')  
      
    return render(request, 'todos/todo_form.html')  
  
# Update existing todo  
def todo_update(request, pk):  
    todo = get_object_or_404(Todo, pk=pk)  
      
    if request.method == 'POST':  
        todo.title = request.POST.get('title')  
        todo.description = request.POST.get('description')  
        todo.completed = request.POST.get('completed') == 'on'  
        todo.save()  
        return redirect('todo_list')  
      
    return render(request, 'todos/todo_form.html', {'todo': todo})  
  
# Delete todo  
def todo_delete(request, pk):  
    todo = get_object_or_404(Todo, pk=pk)  
    if request.method == 'POST':  
        todo.delete()  
        return redirect('todo_list')  
    return render(request, 'todos/todo_confirm_delete.html', {'todo': todo})  
  
# Toggle complete status  
def todo_toggle(request, pk):  
    todo = get_object_or_404(Todo, pk=pk)  
    todo.completed = not todo.completed  
    todo.save()  
    return redirect('todo_list')  