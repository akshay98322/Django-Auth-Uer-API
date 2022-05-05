from django.urls import path
from .views import (UserRegistrationApiView, 
                    UserLoginApiView, 
                    UserProfileApiView, 
                    UserChangePassApiView, 
                    SendPassResetMailApiView)

urlpatterns = [
    path('register/', UserRegistrationApiView.as_view(), name='register'),
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('profile/', UserProfileApiView.as_view(), name='profile'),
    path('changepass/', UserChangePassApiView.as_view(), name='changepass'),
    path('reset-pass/', SendPassResetMailApiView.as_view(), name='reset-pass'),
]
