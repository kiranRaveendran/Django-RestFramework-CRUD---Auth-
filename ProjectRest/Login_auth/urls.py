from django.urls import path
from .views import UserRegistrationView
# , RequestOTPView, VerifyOTPView, LoginView

urlpatterns = [
    path('Auth_register/', UserRegistrationView.as_view(), name='Auth_register'),
    # path('Auth_request_otp/', RequestOTPView.as_view(), name='Auth_request_otp'),
    # path('Auth_verify_otp/', VerifyOTPView.as_view(), name='Auth_verify_otp'),
    # path('Auth_login/', LoginView.as_view(), name='Auth_login'),
]
