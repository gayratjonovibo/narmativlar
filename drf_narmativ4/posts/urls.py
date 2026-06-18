from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import PostViewSet, RegisterAPIView, LoginAPIView, LogoutAPIView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('token/', obtain_auth_token, name='api-token'),

    path('register/', RegisterAPIView.as_view(), name='api-register'),

    path('login/', LoginAPIView.as_view(), name='api-login'),

    path('logout/', LogoutAPIView.as_view(), name='api-logout'),

    path('', include(router.urls)),
]