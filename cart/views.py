from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Cart, CartItem
from products.models import Product

@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        try:
            quantity = int(
                request.POST.get('quantity', 1)
            )

            if quantity <= 0:
                messages.error(
                    request,
                    'Quantity must be greater than zero.'
                )

                return redirect('product_list')

        except (ValueError, TypeError):

            messages.error(
                request,
                'Please enter a valid quantity.'
            )

            return redirect('product_list')

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if created:
            cart_item.quantity = quantity

        else:
            cart_item.quantity += quantity

        cart_item.save()

        messages.success(
            request,
            f'{product.name} added to cart.'
        )

        return redirect('view_cart')

    return redirect('product_list')

@login_required
def view_cart(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = cart.items.select_related(
        'product'
    )

    total = cart.get_total()

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': total,
    }

    return render(
        request,
        'cart/cart.html',
        context
    )

@login_required
def update_cart(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if request.method == 'POST':

        try:
            quantity = int(
                request.POST.get('quantity')
            )

            if quantity <= 0:

                messages.error(
                    request,
                    'Quantity must be greater than zero.'
                )

                return redirect('view_cart')

            cart_item.quantity = quantity
            cart_item.save()

            messages.success(
                request,
                'Cart updated successfully.'
            )

        except (ValueError, TypeError):

            messages.error(
                request,
                'Please enter a valid quantity.'
            )

    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    cart_item.delete()

    messages.success(
        request,
        'Item removed from cart.'
    )

    return redirect('view_cart')  

        