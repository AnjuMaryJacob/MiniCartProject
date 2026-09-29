from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated

from .models import Order, OrderItem
from cart.models import Cart


@login_required
def order_list(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'orders/order_list.html',
        {'orders': orders}
    )


@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'orders/order_detail.html',
        {'order': order}
    )


@login_required
def create_order(request):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    cart_items = cart.items.select_related('product')

    if not cart_items.exists():
        messages.error(
            request,
            'Your cart is empty.'
        )

        return redirect('view_cart')

    if request.method == 'POST':

        total_amount = cart.get_total()

        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount
        )

        for item in cart_items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart.items.all().delete()

        messages.success(
            request,
            f'Order #{order.id} placed successfully.'
        )

        return redirect(
            'order_detail',
            order_id=order.id
        )

    return render(
        request,
        'orders/create_order.html',
        {
            'cart': cart,
            'cart_items': cart_items,
            'total': cart.get_total()
        }
    )

@login_required
def order_update(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if request.method == 'POST':

        status = request.POST.get('status')

        valid_statuses = [
            choice[0]
            for choice in Order.STATUS_CHOICES
        ]

        if status in valid_statuses:

            order.status = status
            order.save()

            messages.success(
                request,
                'Order status updated successfully.'
            )

        else:

            messages.error(
                request,
                'Invalid order status.'
            )

        return redirect(
            'order_detail',
            order_id=order.id
        )

    return render(
        request,
        'orders/order_update.html',
        {
            'order': order,
            'status_choices': Order.STATUS_CHOICES
        }
    )

@login_required
def order_delete(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if request.method == 'POST':

        order.delete()

        messages.success(
            request,
            'Order deleted successfully.'
        )

        return redirect('order_list')

    return render(
        request,
        'orders/order_delete.html',
        {
            'order': order
        }
    )    

class OrderViewSet(viewsets.ModelViewSet):

    serializer_class = OrderSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Order.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )