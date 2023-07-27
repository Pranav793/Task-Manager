from typing import Optional
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.views import LoginView

from tasks.models import Task

def session_storage_view(request):
    total_views = request.session.get("total_views", 0)
    request.session["total_views"] = total_views +1
    return HttpResponse(f"Total views is {total_views}")


# Create your views here.
class UserLoginView(LoginView):
    template_name: str = "user_login.html"

class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name: str = "user_create.html"
    success_url: Optional[str] = "/user/login"



class GenericTaskDeleteView(DeleteView):
    model = Task
    template_name: str = "task_delete.html"
    success_url = "/tasks"

class GenericTaskDetailView(DetailView):
    model = Task
    template_name = "task_detail.html"

class TaskCreateForm(ModelForm):

    def clean_title(self):
        # clean_ + <attribute> gets run automatically
        title = self.cleaned_data["title"]
        if(len(title) < 10):
            raise ValidationError("Data too small")
        return title.upper()

    class Meta:
        model = Task
        fields = ["title", "description", "completed"]
        

class GenericTaskUpdateView(UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "task_update.html"
    success_url = "/tasks"
    

class GenericCreateTaskView(CreateView):
    form_class = TaskCreateForm
    template_name = "task_create.html"
    success_url = "/tasks"


class GenericTaskView(ListView):
    queryset = Task.objects.filter(deleted=False)
    template_name = "tasks.html"
    context_object_name = "tasks"
    paginate_by = 5

    def get_queryset(self):
        search_term = self.request.GET.get("search")
        tasks = Task.objects.filter(deleted=False)
        if search_term:
            tasks = tasks.filter(title__icontains=search_term)
        return tasks

class CreateTaskView(View):
    def get(self, request):
        return render(request, "task_create.html")

    def post(self, request):
        task_value = request.POST.get("task")
        task_obj = Task(title=task_value)
        task_obj.save()
        return HttpResponseRedirect("/tasks")





class TaskView(View):

    def get(self, request):
        search_term = request.GET.get("search")
        tasks = Task.objects.filter(deleted=False)
        if search_term:
            tasks = tasks.filter(title__icontains=search_term)
        return render(request, "tasks.html", {
            "tasks": tasks
        })

    def post(self,request):
        pass

def tasks_view(request):
    search_term = request.GET.get("search")
    tasks = Task.objects.filter(deleted=False)
    if search_term:
        tasks = tasks.filter(title__icontains=search_term)
    return render(request, "tasks.html", {
        "tasks": tasks
    })

def add_task_view(request):
    task_value = request.GET.get("task")
    task_obj = Task(title=task_value)
    task_obj.save()
    return HttpResponseRedirect("/tasks")

def delete_task_view(request, index):
    Task.objects.filter(id=index).update(deleted=True)
    return HttpResponseRedirect("/tasks")
