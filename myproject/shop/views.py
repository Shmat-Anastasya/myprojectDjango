from django.shortcuts import render, get_object_or_404
from .models import Product

def index(request):
    return render(request, 'index.html')

def catalog(request):
    products = Product.objects.all()
    return render(request, 'catalog.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product.html', {'product': product})

def test(request):
    return render(request, 'test.html')
 