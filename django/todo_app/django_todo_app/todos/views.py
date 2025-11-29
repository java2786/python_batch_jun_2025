from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo 
from django.http import HttpResponse

# Create your views here.
# def todos(request):
#     pass 

def todo_list(request):
    todos = Todo.objects.all() 
    return render(request, 'todos/todo_list.html', {'todos': todos})
    

def todo_create(request):
    print("Request method create: ",request.method)
    if request.method == 'POST':
        print("*"*50)
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        Todo.objects.create(
            title=title,
            description=description
        )
        return redirect('todo_list')
        # print(title)
        # print(description)
        # return HttpResponse("<h1>Welcome to Create todo</h1>")
    else:
        return render(request, 'todos/todo_form.html')


def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method=='POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        todo.completed = request.POST.get('completed') == 'on'
        
        todo.save()
        # todo.save(update_fields=['title','description', 'completed'])
        # Todo.objects.filter(pk=pk).update(title='some value')
        return redirect('todo_list')
    else:
        return render(request, 'todos/todo_form.html', {'todo': todo})

def todo_delete(request):
    pass 

def todo_toggle(request):
    pass 
