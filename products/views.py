from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Product
from .forms import ProductForm
from rest_framework import viewsets
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated

def product_list(request):
    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(
        request,
        'products/product_list.html',
        context
    )

def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    recently_viewed = request.session.get(
        'recently_viewed',
        []
    )

    if product_id in recently_viewed:
        recently_viewed.remove(product_id)

    recently_viewed.insert(0, product_id)

    recently_viewed = recently_viewed[:5]

    request.session['recently_viewed'] = recently_viewed

    return render(
        request,
        'products/product_detail.html',
        {'product': product}
    )

def recently_viewed(request):

    product_ids = request.session.get(
        'recently_viewed',
        []
    )

    products = Product.objects.filter(
        id__in=product_ids
    )

    product_dict = {
        product.id: product
        for product in products
    }

    recently_viewed_products = [
        product_dict[product_id]
        for product_id in product_ids
        if product_id in product_dict
    ]

    return render(
        request,
        'products/recently_viewed.html',
        {
            'products': recently_viewed_products
        }
    )    

def product_create(request):

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('product_list')

    else:
        form = ProductForm()

    return render(
        request,
        'product_form.html',
        {'form': form}
    )

def product_update(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product.id)

    else:
        form = ProductForm(instance=product)

    return render(
        request,
        'product_form.html',
        {'form': form}
    )

def product_delete(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(
        request,
        'product_confirm_delete.html',
        {'product': product}
    )  

def product_create(request):

    if request.method == 'POST':

        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            return redirect('product_list')

    else:

        form = ProductForm()

    return render(
        request,
        'products/product_form.html',
        {
            'form': form
        }
    )       

def product_update(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            return redirect('product_detail', product_id=product.id)

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        'products/product_form.html',
        {
            'form': form,
            'product': product
        }
    )

def product_delete(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        product.delete()

        return redirect('product_list')

    return render(
        request,
        'products/product_delete.html',
        {
            'product': product
        }
    )      

class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer

    permission_classes = [
        IsAuthenticated
    ]