from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from task.views import TaskViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# 📌 1. Swagger konfiguratsiyasiga Bearer Security qo'shamiz:
schema_view = get_schema_view(
    openapi.Info(
        title="Task & Post API",
        default_version='v1',
        description="Celery, Redis va Swagger UI Integration",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'posts', TaskViewSet, basename='posts')

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include(router.urls)),

    # 🔥 DRF va Swagger session login ishlashi uchun qo'shing:
    path('accounts/', include('rest_framework.urls')),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]