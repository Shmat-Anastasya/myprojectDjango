from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.forms import UserCreationForm
from accounts.forms import CustomUserCreationForm
from django.http import HttpResponse

from .models import Product, Category, Cart, CartItem, Order, OrderItem, Favorite
import uuid


def index(request):
    return render(request, 'index.html')

def catalog(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Получаем выбранные параметры
    category = request.GET.get('category')
    sort = request.GET.get('sort')

    # Фильтрация по категории
    if category:
        products = products.filter(category__name=category)

    # Сортировка
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')

    # Избранное
    if request.user.is_authenticated:
        favorite_ids = set(
            Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
        )
    else:
        favorite_ids = set()

    return render(request, 'catalog.html', {
        'products': products,
        'categories': categories,
        'current_category': category,
        'current_sort': sort,
        'favorite_ids': favorite_ids,
    })


# стр товара
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()

    return render(request, 'product.html', {
        'product': product,
        'is_favorite': is_favorite,
    })

# # регист
# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()          
#             return redirect('profile')  
#     else:
#         form = CustomUserCreationForm()

#     return render(request, 'register.html', {'form': form})

# # лк
# def profile(request):
#     return render(request, 'profile.html')

#корзина
def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Получаем корзину пользователя
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Все товары в корзине
    items = CartItem.objects.filter(cart=cart)

    # Добавляем вычисляемое поле total_price
    for item in items:
        item.total_price = item.price_at_moment * item.quantity

    # Итоговая сумма корзины
    total = sum(item.total_price for item in items)

    return render(request, 'cart.html', {
        'items': items,
        'total': total,
    })

# добавл тов
def add_to_cart(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    product = get_object_or_404(Product, pk=pk)

    #актив корзина
    cart, created = Cart.objects.get_or_create(user=request.user, status='active')

    # Создаём или обновляем CartItem
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'price_at_moment': product.price}
    )

    if not created:
        item.quantity += 1

    item.save()
    return redirect('cart')

# удал тов
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')

# измен кол-ва
def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart')


def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    # Если количество больше 1 — уменьшаем
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        # Если 1 — удаляем товар
        item.delete()

    return redirect('cart')

# избран
def favorites(request):
    if not request.user.is_authenticated:
        return redirect('login')

    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites.html', {'favorites': favorites})

# оформ заказа
def make_order(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Получаем активную корзину
    cart, created = Cart.objects.get_or_create(user=request.user, status='active')
    items = CartItem.objects.filter(cart=cart)

    # Если корзина пустая — возвращаемся
    if not items:
        return redirect('cart')

    # Итоговая сумма заказа
    total = sum(item.price_at_moment * item.quantity for item in items)

    # Создаём заказ
    order = Order.objects.create(
        user=request.user,
        receipt_number=uuid.uuid4().hex[:10],  # Генерация номера чека
        total=total
    )

    # Переносим товары в OrderItem
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price_at_moment=item.price_at_moment
        )

    # Очищаем корзину
    items.delete()

    return redirect('orders')

# ист заказов
def orders(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Все заказы
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'orders.html', {'orders': orders})

def toggle_favorite(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    product = get_object_or_404(Product, pk=pk)

    fav, created = Favorite.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        fav.delete()

    return redirect(request.META.get('HTTP_REFERER', 'catalog'))
