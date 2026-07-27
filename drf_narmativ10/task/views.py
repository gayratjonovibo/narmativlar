from rest_framework import viewsets, permissions
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from django.core.cache import cache
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    cache_response_timeout = 60

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        self.clear_posts_cache()

    def perform_update(self, serializer):
        serializer.save()
        self.clear_posts_cache()

    def perform_destroy(self, instance):
        instance.delete()
        self.clear_posts_cache()

    def clear_posts_cache(self):
        cache.clear()