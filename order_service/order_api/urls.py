from django.urls import path
from . import views

urlpatterns = [
    #path('<str:order_uid>/warranty', views),
    path('<str:userUid>', views.get_post_orders),
    #path('<str:user_uid>/<str:order_uid>', views),
    path('<str:userUid>/<str:orderUid>', views.get_order),
]