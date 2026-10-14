from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart-detail'),
    path('add/<int:item_id>/', views.add_to_cart, name='add-to-cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('update/<int:item_id>/', views.update_cart_item, name='update-cart-item'),
]