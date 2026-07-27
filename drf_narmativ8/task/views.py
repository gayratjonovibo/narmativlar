from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly

from .models import Task
from .serializers import TaskSerializer

from .tasks import send_post_creation_log


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.select_related('author').all().order_by('-id')
    serializer_class = TaskSerializer

    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    filterset_fields = ['title', 'created_at']
    ordering_fields = ['created_at', 'title']

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        send_post_creation_log.delay(instance.id, instance.title)


# task/views.py ichida:
from .tasks import send_post_creation_log  # 🔥 Import qiling


