from django.urls import path
from .views import PostListCreateAPIView, PostDetailAPIView

urlpatterns = [
    # /api/posts/
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    # /api/posts/<id>/
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
]