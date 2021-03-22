
from django.urls import path, include
from . import views

urlpatterns = [
    
    path('login/', views.login),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
]
