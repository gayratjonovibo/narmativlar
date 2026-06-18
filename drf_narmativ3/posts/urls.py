from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, RegisterAPIView, LoginAPIView, LogoutAPIView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api-register'),   # Manzil: /api/register/
    path('login/', LoginAPIView.as_view(), name='api-login'),             # Manzil: /api/login/
    path('logout/', LogoutAPIView.as_view(), name='api-logout'),           # Manzil: /api/logout/

    path('', include(router.urls)),                                        # Manzil: /api/posts/
]