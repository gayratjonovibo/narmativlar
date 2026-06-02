from django.urls import path
from .views import ForgotPasswordView, RestorePasswordView

urlpatterns = [
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('restore-password/', RestorePasswordView.as_view(), name='restore_password'),
]