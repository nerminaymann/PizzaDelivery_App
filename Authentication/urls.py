from django.urls import path,include
from .views import Authentication, SignUp

urlpatterns = [
    path('',Authentication.as_view(),name='hello_authentication'),
    path('signup/',SignUp.as_view(),name='signup')
]