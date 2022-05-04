from django.urls import path
from .views import UserRegistrationApiView, UserLoginApiView

urlpatterns = [
    path('register/', UserRegistrationApiView.as_view(), name='register'),
    path('login/', UserLoginApiView.as_view(), name='login'),
]
