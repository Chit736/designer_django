from django.contrib import admin
from apps.orders.models import OrderModel, OrderItemModel

class OrderItemInline(admin.TabularInline):
    model = OrderItemModel
    extra = 0

# Register your models here.
admin.site.register(OrderModel)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'total_price', 'status', 'is_paid', 'created_at') # status ကို ထည့်တယ်
    list_filter = ('status', 'is_paid', 'created_at')
    list_editable = ('status', 'is_paid') #List ကနေတင် တိုက်ရိုက် ပြောင်းလို့ရအောင်
    inlines = [OrderItemInline]


