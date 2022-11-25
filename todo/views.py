from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Todo
from django.template import loader


# Create your views here.
def index(request):
    #model = Todo
    #context_object_name = 'todo_listesi'     
    queryset=Todo.objects.all()
    template_name = 'todo/index.html'
    context={ 'todo_listesi': queryset}
    loader.get_template('todo/yapilacaklar.html')
    return render(request, template_name, context)

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Kayıt başarılı." )
			return redirect(index)
		messages.error(request, "Kayıt başarısız. Geçersiz bilgi.")
	form = NewUserForm()
	return render (request=request, template_name="todo/register.html", context={"register_form":form})

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
        
				redirect(index)
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="todo/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("todo:index")