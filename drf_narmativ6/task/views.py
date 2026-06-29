from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

# 📌 6-bosqich uchun kerakli DRF va Custom permission importlari:
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly  # ← 5-bosqichda ochgan permissions.py faylingdan

from .models import Task
from .serializers import TaskSerializer


# 📌 4-bosqich (5-normativdan): Maxsus sahifalash klassi
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all().order_by('-id')
    serializer_class = TaskSerializer
    pagination_class = StandardResultsSetPagination

    # 📌 6-bosqich (Yangi): Permissionlarni ulash
    # IsAuthenticatedOrReadOnly -> GET hamma uchun, qolgan so'rovlar faqat login qilganlarga
    # IsOwnerOrReadOnly -> PUT/PATCH/DELETE faqat post egasiga
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # 📌 5-normativdagi filter sozlamalari (o'zgarishsiz qoladi)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    filterset_fields = ['title', 'created_at']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    # 📌 4-bosqich (Yangi): Post yaratilayotganda avtomatik authorni request.user-ga bog'lash
    def perform_create(self, serializer):
        # Agar sening Task modelingdagi maydon nomi 'owner' bo'lsa owner=self.request.user qilgin, 'author' bo'lsa author=...
        serializer.save(author=self.request.user)