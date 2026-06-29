from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import Task  # Model nomingiz (Task yoki Post)
from .serializers import TaskSerializer


# 📌 4-bosqich: Har bir viewset uchun maxsus sahifalash klassi (ixtiyoriy, settings.py dynamic bo'ladi)
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Har sahifada 10 tadan ma'lumot chiqadi
    page_size_query_param = 'page_size'
    max_page_size = 100


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all().order_by('-id')  # default xatoliklarni oldini olish uchun tartiblash
    serializer_class = TaskSerializer
    pagination_class = StandardResultsSetPagination  # Maxsus sahifalashni ulaymiz

    # 📌 6-bosqich: filter_backends ro'yxatini sozlash
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # 📌 1-bosqich: Search qidiruv maydonlari (title va content bo'yicha)
    # Agar modelingizda name va description bo'lsa: ['name', 'description'] qiling
    search_fields = ['title', 'content']

    # 📌 2-bosqich: Aniq qiymat bo'yicha filter qilish (Query params uchun)
    filterset_fields = ['title', 'created_at']

    # 📌 3-bosqich: Ordering (Tartiblash) maydonlari
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']  # Default holatda yangi qo'shilganlar tepada chiqadi