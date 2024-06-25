from django.urls import path,include
from .views import OrderList,OrderDetail,UpdateStatus_CheckOutButton

urlpatterns = [
    path('',OrderList.as_view(),name='orders'),
    path('<int:pk>/',OrderDetail.as_view(),name='order_detail'),
    path('update-status/<int:pk>',UpdateStatus_CheckOutButton.as_view(),name='update_status')
]