from django.shortcuts import render, redirect, get_object_or_404
from apps.categories.models import CategoryModel
from apps.products.models import ProductModel

def product_list(request):
    products = ProductModel.objects.all().order_by("-created_at")
    context = {
        "products": products,
    }

    return render(request, "product_list.html", context)

def product_create(request):
    categories = CategoryModel.objects.all()
    if request.method == "POST":
        title = request.POST.get("title")
        price = request.POST.get("price")
        qty = request.POST.get('qty')
        image = request.FILES.get('image')
        description = request.POST.get("description")
        category = request.POST.get("category")

        ProductModel.objects.create(
            title = title,
            price = price,
            qty = qty,
            image = image,
            description = description,
            category_id = category,
        )
        return redirect('product_list')
    context = {
        "categories": categories,
    }
    return render(request, "product_create.html", context)

def product_edit(request, pk):
    products = get_object_or_404(ProductModel, id=pk)
    categories = CategoryModel.objects.all()
    if request.method == "POST":
        products.title = request.POST.get("title")
        products.price = request.POST.get("price")
        products.qty = request.POST.get("qty")
        if request.FILES.get("image"):
            products.image.delete(save=False)
            products.image = request.FILES.get("image")
        products.description = request.POST.get("description")
        products.save()
        return redirect("product_list")
    context = {
        "products": products,
        "categories": categories,
    }
    return render(request, "product_edit.html", context)

def product_delete(request, pk):
    products = get_object_or_404(ProductModel, id=pk)
    if products.image:
        products.image.delete(save=False)
    products.delete()
    return redirect("product_List")