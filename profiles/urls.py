from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.profile_detail,
        name='profile_detail'
    ),

    path(
        'create/',
        views.profile_create,
        name='profile_create'
    ),

    path(
        'update/',
        views.profile_update,
        name='profile_update'
    ),

    path(
        'delete/',
        views.profile_delete,
        name='profile_delete'
    ),

]