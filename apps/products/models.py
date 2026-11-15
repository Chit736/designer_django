from django.db import models
from apps.categories.models import CategoryModel

# Create your models here.
class ProductModel(models.Model):
    title = models.CharField(max_length = 255)
    price = models.IntegerField()
    qty = models.IntegerField()
    image = models.ImageField(upload_to = "products/", null=True, blank= True)
    description = models.TextField(null=True, blank = True)
    category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, null=True, blank = True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.title} - {self.price}"
