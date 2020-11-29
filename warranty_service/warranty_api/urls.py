from django.urls import path
from . import views

urlpatterns = [
    path('<str:itemUid>',views.get_post_del),
    path('<str:itemUid>/warranty',views.req_warranty)
]
