from django.urls import path
from . import views

urlpatterns = [
    path('', views.take_item),
    path('<str:orderItemUid>', views.get_del_ware),
    path('<str:orderItemUid>/warranty', views.req_warr)
]