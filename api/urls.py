
from django.urls import path, include
from . import views

urlpatterns = [
    
    # path('login/', views.login),
    path('registerview/', views.RegisterView.as_view(), name='auth_register'),
    path('register/', views.Register.as_view(), name = 'Unserialized Register'),
    path('verifyotp/', views.Verify.as_view(), name = 'Otp Vrification'),
    path('login/', views.loginview.as_view(), name  = 'logging a user in'),
    path('logout/', views.logout.as_view(), name  = 'logging out a user '),
    path('createtoken/', views.CreateToken.as_view(), name  = 'testing creation of Token'),
    

]
