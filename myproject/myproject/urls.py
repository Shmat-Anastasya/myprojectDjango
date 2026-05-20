"""
URL configuration for myproject project.

Основной файл маршрутизации:
- подключает админку
- подключает страницы магазина
- подключает авторизацию
- подключает корзину, избранное, заказы
"""

from django.contrib import admin
from django.urls import path, include
from shop import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    #админ
    path('admin/', admin.site.urls),

    path('', views.index),                    
    path('catalog/', views.catalog),          
    path('product/<int:pk>/', views.product_detail),  
    #path('test/', views.test),                 

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('register/', views.register, name='register'),

    # path('profile/', views.profile, name='profile'),

    path('cart/', views.cart, name='cart'),                        # Страница корзины
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),  # Добавить товар
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Удалить товар
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),  # +
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),  # –

    path('favorites/', views.favorites, name='favorites'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),

    path('orders/', views.orders, name='orders'),          # История заказов
    path('order/make/', views.make_order, name='make_order'),  # Оформление заказа

    # accounts
   path('', include('accounts.urls')),

]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
