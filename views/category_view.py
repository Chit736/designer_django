from django.shortcuts import render, redirect, get_object_or_404
from apps.categories.models import CategoryModel
from django.contrib import messages


def category_list(request):
    categories = CategoryModel.objects.all().order_by("-created_at")
    return render(request, "category_list.html",{"categories":categories})


def category_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        CategoryModel.objects.create(
            name = name
        )
        messages.success(request, "Category added successfully!")
        return redirect("category_list")
    return render(request, "category_create.html")

def category_toggle_status(request, pk):
    category = get_object_or_404(CategoryModel, id=pk)
    if category.status == CategoryModel.StatusChoices.ACTIVE:
        category.status = CategoryModel.StatusChoices.INACTIVE
        messages.warning(request, "Category status changed to Inactive.")
    else:
        category.status = CategoryModel.StatusChoices.ACTIVE
        messages.success(request, "Category status changed to Active.")
    category.save()
    return redirect("category_list")


def category_edit(request, pk):
    category = get_object_or_404(CategoryModel, id = pk)
    if request.method == "POST":
        category.name = request.POST.get('name')
        category.save()
        messages.warning(request, "Edit category successfully!")
        return redirect("category_list")
    return render(request, "category_edit.html",{"category":category})

def category_delete(request, pk):
    category = get_object_or_404(CategoryModel, id = pk)
    category.delete()
    messages.error(request, "Category deleted successfully!")
    return redirect("category_list")