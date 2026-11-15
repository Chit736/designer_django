from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.orders.models import OrderModel, OrderItemModel
from apps.carts.models import CartModel

@login_required
def checkout(request):
    cart, created = CartModel.objects.get_or_create(user = request.user)
    products = cart.products.all()

    if not products:
        messages.warning(request, "သင့်စျေးဝယ်စာရင်းထဲမှာ ပစွည်းမရှိပါဘူး။")
        return redirect("cart_list")

    total_price = sum(item.price for item in products)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        order = OrderModel.objects.create(
            user = request.user, 
            full_name = full_name,
            phone = phone,
            address = address,
            total_price = total_price,
        )

        for product in products:
            # stock လုံလောက်မူရှိ မရှိ အရင်စစ်မယ် 
            if product.qty < 1:
                messages.error(request, f"'{product.title}' ပစွည်း လက်ကျန်မရှိတော့ပါဘူး။")
                order.delete()
                return redirect("cart_list")

            # order Item ကို ဖန်တီးမယ် 
            OrderItemModel.objects.create(
                order = order,
                product = product,
                price = product.price,
                quantity = 1,
            )

            # product ရဲ့ stock ကို ၁ ခု လျှော့မယ် 
            product.qty -= 1
            product.save()
            
        cart.products.clear()
    
        messages.success(request, "အော်ဒါ တင်ခြင်း အောင်မြင်ပါတယ်။")
        return redirect("order_success", order_id = order.id)

    context = {
    "products": products,
    "total_price": total_price,
    }
    return render(request, "checkout.html", context)

@login_required
def order_success(request, order_id):
    order = get_object_or_404(OrderModel, id=order_id, user=request.user)
    return render(request, "order_success.html", {"order": order})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(OrderModel, id=order_id, user=request.user)

    items = order.items.all()

    context = {
        "order": order, 
        "items": items,
    }
    return render(request, "order_detail.html", context)

@login_required
def my_order(request):
    if request.user.is_staff:
        orders = OrderModel.objects.all().order_by('-created_at')
    else:
        orders = OrderModel.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "my_order.html", {"orders": orders})


