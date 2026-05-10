from django.shortcuts import render, redirect, get_object_or_404
from .models import Post


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})


def post_create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')  # Rasm faylini olish
        Post.objects.create(title=title, content=content, image=image)
        return redirect('post_list')
    return render(request, 'post_form.html')


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})



