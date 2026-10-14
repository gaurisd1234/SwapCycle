from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from .models import Cart, CartItem
from marketplace.models import Item

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{item.title} added to cart.")
    return redirect(request.META.get('HTTP_REFERER', reverse('cart:cart-detail')))

@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(Item, id=item_id)
    try:
        cart_item = CartItem.objects.get(cart=cart, item=item)
        cart_item.delete()
        messages.success(request, f"{item.title} removed from cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in cart.")
    
    return redirect('cart:cart-detail')

@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, item_id=item_id)
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated successfully.")
        else:
            cart_item.delete()
            messages.success(request, f"{cart_item.item.title} removed from cart.")
            
        return redirect('cart:cart-detail')
    return JsonResponse({"error": "Invalid request"}, status=400)
