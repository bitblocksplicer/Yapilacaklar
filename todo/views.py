from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Todo, ToDoList, ToDoItem
from django.template import loader
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView)
from django.urls import reverse, reverse_lazy


# Create your views here.
def index(request):
    #model = Todo
    #context_object_name = 'todo_listesi'
    queryset = Todo.objects.all()
    template_name = 'todo/index.html'
    context = {'todo_listesi': queryset}
    loader.get_template('todo/yapilacaklar.html')
    return render(request, template_name, context)


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Kayıt başarılı.")
            return redirect('todo:index')
        else:
            messages.error(request, "Kayıt başarısız. Geçersiz bilgi.")
            return redirect('todo:register')
    else:
        form = NewUserForm()
        return render(request=request,
                      template_name="todo/register.html",
                      context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"{username} olarak giriş yaptınız.")
                return redirect('todo:index')
            else:
                messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
                return redirect('todo:index')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
            return redirect('todo:login')
    else:
        form = AuthenticationForm()
        return render(request=request,
                      template_name="todo/login.html",
                      context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Başarıyla çıkış yaptınız.")
    return redirect("todo:index")


def denemelere(request):
    return render(request, "todo/deneme.html")


class ListListView(ListView):
    model = ToDoList
    template_name = "todo/index.html"


class ItemListView(ListView):
    model = ToDoItem
    template_name = "todo/todo_list.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context


class ListCreate(CreateView):
    model = ToDoList
    fields = ["title"]

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context["title"] = "Yeni bir liste oluştur"
        return context


class ItemCreate(CreateView):
    model = ToDoItem
    fields = '__all__'

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data

    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Yeni Bir Öğe Oluştur"
        return context

    def get_success_url(self):
        return reverse("todo:list", args=[self.object.todo_list_id])


class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Öğeyi Düzenle"
        return context

    def get_success_url(self):
        return reverse("todo:list", args=[self.object.todo_list_id])


class ListDelete(DeleteView):
    model = ToDoList
    # You have to use reverse_lazy() instead of reverse(),
    # as the urls are not loaded when the file is imported.
    success_url = reverse_lazy("todo:index")


class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("todo:list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context
