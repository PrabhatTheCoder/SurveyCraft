from django.db import models
import uuid
# Create your models here.
    
class App(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    URL = models.URLField()
    app_details = models.TextField()
    isActive = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class AppScreen(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    App = models.ForeignKey(App, on_delete=models.CASCADE)
    Image = models.ImageField(upload_to="app_screens/")

    class Meta:
        unique_together = ("name", "App")