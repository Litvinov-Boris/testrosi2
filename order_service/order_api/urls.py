from django.urls import path
from . import views

urlpatterns = [
    path('<str:orderUid>/warranty', views.get_warranty),
    path('<str:userUid>', views.get_post_orders),
    path('<str:userUid>/<str:orderUid>', views.get_order),
]