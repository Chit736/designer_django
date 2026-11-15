from django.shortcuts import render, redirect, get_object_or_404
from views import page_view
from apps.categories.models import CategoryModel
from apps.products.models import ProductModel
from apps.carts.models import CartModel
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages

from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import send_mail
import string
import secrets

def index(request):
    products = ProductModel.objects.all()
    categories = CategoryModel.objects.all()

    category_id = request.GET.get("category","")
    search = request.GET.get("search","").strip()

    if category_id:
        products = products.filter(category_id = category_id)

    if search:
        products = products.filter(Q(title_icontains = search)|Q(category_name_icontains = search))

    paginator = Paginator(products, 4)
    page_number = request.GET.get("page")
    product_page = paginator.get_page(page_number)

    context = {
        "products": product_page,
        "categories": categories,
        "selected_category": category_id,
    }
    return render(request, "index.html", context)

def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Password doesn't match")
            return redirect("register")
        if User.objects.filter(username = username).exists():
            messages.error(request, "Username is already exists")
            return redirect("register")

        else:
            alphabet = string.ascii_uppercase + string.digits
            otp = ''.join(secrets.choice(alphabet) for i in range (8))
            request.session['user_data'] = {
                'username': username,
                'password': password,
                'email': email,
                'otp': otp,
            }
            send_mail(
                'Your Verivication Code',
                f'Your verivication code is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                recipient_list = [email],
                fail_silently = False,
            )
            messages.success(request, "Your code is send to your email, Please Check...")
            return redirect("verify_otp")

        user = User.objects.create_user(
            username = username,
            email = email,
            password = password
        )
        messages.success(request, "Register Successfully!")
        return redirect("login")
        
    return render(request, "register.html")

def verify_otp(request):
    if 'user_data' not in request.session:
        return redirect("register")
    if request.method == "POST":
        user_otp = request.POST.get("otp")


        user_data = request.session["user_data"]
        
        if user_otp == user_data["otp"]:
            User.objects.create_user(
                username = user_data["username"],
                email = user_data["email"],
                password = user_data["password"]
            )
            messages.success(request, "Register is done")
        else:
            messages.error(request, "Invalid otp")
    return render(request, "verify_otp.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login is successfully!")
            return redirect("index")
        else:
            messages.error(request, "Invail username or password")
    return render(request, "login.html")

def user_logout(request):
    logout(request)
    messages.success(request, "Logout is successfully!")
    return redirect("login")

@login_required
def cart_list(request):
    
    cart, created = CartModel.objects.get_or_create(user = request.user)
    products = cart.products.all()

    total_price = sum(item.price for item in products)
    context = {
        "products": products,
        "total_price": total_price,
    }
    return render(request, "cart_list.html", context)

@login_required
def add_to_cart(request, pk):
    products = get_object_or_404(ProductModel, id=pk)
    cart, created = CartModel.objects.get_or_create(user = request.user)
    cart.products.add(products)
    messages.success(request, "Add to cart Successfully!")
    return redirect("cart_list")
    return render(request, "add_to_cart.html")

def remove_cart(request, pk):
    products = get_object_or_404(ProductModel, id=pk)
    cart, created = CartModel.objects.get_or_create(user=request.user)
    cart.products.remove(products)
    messages.success(request, "Remove_cart Successfully!")
    return redirect("cart_list")