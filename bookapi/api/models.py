from django.db import models

# Create your models here.
class Book(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return self.title