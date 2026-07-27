from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 🔥 6-bosqich: ViewSet importi (absolute yo'li bilan)
from task.views import TaskViewSet

# 📌 3-bosqich: Simple JWT importlari
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# 📌 7-bosqich: Swagger uchun kerakli importlar
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger konfiguratsiyasi
schema_view = get_schema_view(
    openapi.Info(
        title="Task & Post API",
        default_version='v1',
        description="6-Normativ: Custom Permission, JWT Authentication va Swagger UI",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Router sozlamalari (/api/posts/ ko'rinishida ishlashi uchun)
router = DefaultRouter()
router.register(r'posts', TaskViewSet, basename='posts')

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Router manzillari
    path('api/', include(router.urls)),

    # 📌 3-bosqich: JWT token olish va yangilash endpointlari
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 📌 7-bosqich: Swagger hujjatlashtirish sahifasi
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]