"""
URL configuration for apple project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from views import page_view, category_view, product_view, cart_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', page_view.index, name ="index"),
    path('verify/otp/',page_view.verify_otp, name = "verify_otp"),

    path('register/', page_view.user_register, name ="register"),
    path('login/',page_view.user_login, name ="login"),
    path('logout/',page_view.user_logout, name = "logout"),

    path('categories/', category_view.category_list, name = "category_list"),
    path('categories/toggle-status/<int:pk>/', category_view.category_toggle_status, name = "category_toggle_status"),
    path('categories/create/',category_view.category_create, name = "category_create"),
    path('categories/edit/<int:pk>/', category_view.category_edit, name = "category_edit"),
    path('categories/delete/<int:pk>/', category_view.category_delete, name = "category_delete"),

    path('products/', product_view.product_list, name = "product_list"),
    path('products/create/', product_view.product_create, name="product_create"),
    path('products/edit/<int:pk>/', product_view.product_edit, name="product_edit"),
    path('products/delete/<int:pk>/', product_view.product_delete, name="product_delete"),

    path('carts/', page_view.cart_list, name="cart_list"),
    path('add_to_cart/<int:pk>/',page_view.add_to_cart , name="add_to_cart"),
    path('remove_cart/<int:pk>/', page_view.remove_cart, name="remove_cart"),

    path('checkout/', cart_view.checkout, name="checkout"),
    path('order_success/<int:order_id>/', cart_view.order_success, name="order_success"),
    path('order_detail/<int:order_id>/', cart_view.order_detail, name="order_detail"),
    path('my_orders/', cart_view.my_order, name="my_order"),

] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

