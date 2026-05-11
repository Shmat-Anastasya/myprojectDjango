from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse

from .models import Product, Category, Cart, CartItem
from .models import Order, OrderItem
import uuid


# ГЛАВНАЯ СТРАНИЦА
def index(request):
    return render(request, 'index.html')

# КАТАЛОГ ТОВАРОВ + ФИЛЬТРАЦИЯ + СОРТИРОВКА
def catalog(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Получаем выбранные параметры
    category = request.GET.get('category')
    sort = request.GET.get('sort')

    # --- Фильтрация по категории ---
    if category:
        products = products.filter(category__name=category)

    # --- Сортировка ---
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')

    return render(request, 'catalog.html', {
        'products': products,
        'categories': categories,
        'current_category': category,
        'current_sort': sort,
    })

# СТРАНИЦА ОДНОГО ТОВАРА
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product.html', {'product': product})

# ТЕСТОВАЯ СТРАНИЦА (можно удалить)
def test(request):
    return render(request, 'test.html')

# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        # Если форма валидна — создаём пользователя
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

# ЛИЧНЫЙ КАБИНЕТ

def profile(request):
    return render(request, 'profile.html')

# КОРЗИНА: ОТОБРАЖЕНИЕ
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

# КОРЗИНА: ДОБАВЛЕНИЕ ТОВАРА
def add_to_cart(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    product = get_object_or_404(Product, pk=pk)

    # Получаем активную корзину
    cart, created = Cart.objects.get_or_create(user=request.user, status='active')

    # Создаём или обновляем CartItem
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'price_at_moment': product.price}
    )

    # Если товар уже есть — увеличиваем количество
    if not created:
        item.quantity += 1

    item.save()
    return redirect('cart')

# КОРЗИНА: УДАЛЕНИЕ ТОВАРА
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')

# КОРЗИНА: ИЗМЕНЕНИЕ КОЛИЧЕСТВА
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

# ИЗБРАННОЕ (пока пусто)
def favorites(request):
    return render(request, 'favorites.html')

# ОФОРМЛЕНИЕ ЗАКАЗА
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

# ИСТОРИЯ ЗАКАЗОВ
def orders(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Все заказы пользователя
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'orders.html', {'orders': orders})
