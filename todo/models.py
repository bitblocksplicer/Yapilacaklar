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