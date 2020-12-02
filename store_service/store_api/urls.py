from django.urls import path
from . import views

urlpatterns = [
    path('<str:userUid>/orders', views.get_orders),
    path('<str:userUid>/<str:orderUid>', views.get_order),
    path('<str:userUid>/<str:orderUid>/warranty', views.req_warranty),
    path('<str:userUid>/purchase', views.get_orders),
    path('<str:userUid>/<str:orderUid>/refund', views.req_warranty)
]