from django.urls import path,include
from .views import OrderList

urlpatterns = [
    path('',OrderList.as_view(),name='orders'),
]