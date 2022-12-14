from django.utils import timezone
from django.db import models
from django.urls import reverse


# Create your models here.
class Todo(models.Model):
    baslik = models.CharField(max_length=120)
    aciklama = models.TextField()
    tamamlandi = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return self.baslik


def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)


class ToDoList(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse("todo:list", args=[self.id])

    def __str__(self):
        return self.title


class ToDoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=one_week_hence)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("todo:item-update",
                       args=[str(self.todo_list.id),
                             str(self.id)])

    def __str__(self):
        return f"{self.title}: {self.due_date} Tarihinde sona eriyor"

    class Meta:
        ordering = ["due_date"]
