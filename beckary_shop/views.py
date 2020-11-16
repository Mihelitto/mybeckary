from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Category, Section
from cart.forms import CartAddProductForm



def sec_list(request):
    sec_list = Section.objects.all()
    return render(request, 'product/cat_list.html', {'cat_list': sec_list})

def cat_list(request, slug):
    sec = Section.objects.get(slug = slug)
    cat_list = Category.objects.filter(section_id = sec.id)
    return render(request, 'product/cat_list.html', {'cat_list': cat_list, 'sec':sec})

def prod_list(request, sec_slug, cat_slug):
    cat = Category.objects.get(slug = cat_slug)
    prod_list = Product.objects.filter(category_id = cat.id)
    paginator = Paginator(prod_list, 5)
    page = request.GET.get('page')
    try:
        prods = paginator.page(page)
    except PageNotAnInteger:
        prods = paginator.page(1)
    except EmptyPage:
        prods = paginator.page(paginator.num_pages)

    return render(request, 'product/prod_list.html', {'page':page,'prods': prods, 'cat':cat})

def prod_detail(request, sec_slug, cat_slug, prod_slug):
    cart_product_form = CartAddProductForm()
    prod = get_object_or_404(Product, slug = prod_slug)
    return render(request, 'product/prod_detail.html', {'prod':prod, 'cart_product_form':cart_product_form})


# Create your views here.
