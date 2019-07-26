from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
class Product(models.Model):

    name = models.CharField(max_length=100, blank=False)
    sku = models.SlugField(unique=True, blank=False)
    description = models.TextField(blank=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
