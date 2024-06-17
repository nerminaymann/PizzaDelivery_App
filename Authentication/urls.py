from django.urls import path,include
from .views import AuthenticationList

urlpatterns = [
    path('',AuthenticationList.as_view(),name='orders'),
]