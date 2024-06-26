from django.urls import path,include

from .views import Authentication, SignUp,Login

urlpatterns = [
    path('',Authentication.as_view(),name='hello_authentication'),
    path('signup/',SignUp.as_view(),name='signup'),
    path('login/',Login.as_view(),name='login')
]