from django.contrib import admin
from .models import Todo,ToDoItem, ToDoList

admin.site.register(ToDoItem)
admin.site.register(ToDoList)

class TodoAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'aciklama', 'tamamlandi')

# Register your models here.

admin.site.register(Todo, TodoAdmin)