from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    r'api/orders',
    views.OrderViewSet,
    basename='order'
)

urlpatterns = [

    path(
        '',
        views.order_list,
        name='order_list'
    ),

    path(
        'create/',
        views.create_order,
        name='create_order'
    ),

    path(
    '<int:order_id>/update/',
    views.order_update,
    name='order_update'
    ),

    path(
    '<int:order_id>/delete/',
    views.order_delete,
    name='order_delete'
    ),

    path(
        '<int:order_id>/',
        views.order_detail,
        name='order_detail'
    ),

    # REST API
    path(
        '',
        include(router.urls)
    ),

]