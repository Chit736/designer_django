from django.db import models

# Create your models here.
class CategoryModel(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
    name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    status = models.CharField(
        max_length = 10,
        choices = StatusChoices.choices,
        default = StatusChoices.ACTIVE,
    )

    def __str__(self):
        return self.name
