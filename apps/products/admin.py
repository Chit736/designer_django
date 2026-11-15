from django.contrib import admin
from apps.products.models import ProductModel

# Register your models here.
admin.site.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'qty', 'created_at')
    list_filter = ('category',)
    search_fields = ('title',)
