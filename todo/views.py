from multiprocessing import context
from turtle import title
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .forms import TodoForm
from .models import Todo
from django.urls import reverse

# Show the completed, incompleted and remaining todos


def get_todos_filter(request, all_todos):
    if request.GET and request.GET.get('filter'):
        if request.GET.get('filter') == 'completed':
            return all_todos.filter(is_completed=True)
        if request.GET.get('filter') == 'incompleted':
            return all_todos.filter(is_completed=False)
    return all_todos


def index(request):
    all_todo = Todo.objects.all()
    completed_count = all_todo.filter(is_completed=True).count()
    incompleted_count = all_todo.filter(is_completed=False).count()
    all_count = all_todo.count()

    context = {
        'all_todo': get_todos_filter(request, all_todo),
        'completed_count': completed_count,
        'incompleted_count': incompleted_count,
        'all_count': all_count,
    }
    return render(request, 'todo/index.html', context)


def create_todo(request):
    form = TodoForm()
    context = {'form': form}

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed', False)
        todo = Todo()
        todo.title = title
        todo.description = description
        todo.is_completed = True if is_completed == "on" else False
        todo.save()
        return HttpResponseRedirect(reverse('todo', kwargs={'id': todo.pk}))

    return render(request, 'todo/create-todo.html', context)


def todo_details(request, id):
    todo = get_object_or_404(Todo, pk=id)
    context = {'todo': todo}
    return render(request, 'todo/todo-details.html', context)


def todo_delete(request, id):
    todo = get_object_or_404(Todo, pk=id)
    context = {'todo': todo}
    if request.method == 'POST':
        todo.delete()
        return HttpResponseRedirect(reverse('home'))
    return render(request, 'todo/todo-delete.html', context)


def edit_todo(request, id):
    todo = get_object_or_404(Todo, pk=id)
    form = TodoForm(instance=todo)
    context = {'todo': todo, 'form': form}

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed', False)
        todo.title = title
        todo.description = description
        todo.is_completed = True if is_completed == "on" else False
        todo.save()
        return HttpResponseRedirect(reverse('todo', kwargs={'id': todo.pk}))
        
    return render(request, 'todo/todo-edit.html', context)
