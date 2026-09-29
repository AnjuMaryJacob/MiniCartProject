from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    r'api/products',
    views.ProductViewSet,
    basename='product'
)

urlpatterns = [
    path('', views.product_list, name='product_list'),

    path(
    'product/<int:product_id>/',
    views.product_detail,
    name='product_detail'
),
    path(
    'recently-viewed/',
    views.recently_viewed,
    name='recently_viewed'
),

path(
    'create/',
    views.product_create,
    name='product_create'
),

path(
    'product/<int:product_id>/update/',
    views.product_update,
    name='product_update'
),

path(
    'product/<int:product_id>/delete/',
    views.product_delete,
    name='product_delete'
),

path(
        '',
        include(router.urls)
    ),

]