
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Post


def post_list(request):
    query = request.GET.get('q', '')  # Search so'rovini olish

    # 1-bosqich: Search (qidiruv)
    if query:
        posts_list = Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query)
    else:
        posts_list = Post.objects.all().order_by('-created_at')

    # 2-bosqich: Pagination (sahifalash) - har sahifada 5 tadan
    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/post_list.html', {
        'page_obj': page_obj,
        'query': query  # Qidiruv so'zini templatega qaytaramiz
    })