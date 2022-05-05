from django.urls import path
from .views import UserRegistrationApiView, UserLoginApiView, UserProfileApiView

urlpatterns = [
    path('register/', UserRegistrationApiView.as_view(), name='register'),
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('profile/', UserProfileApiView.as_view(), name='profile'),
]
