from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required # Yangi import
from .models import Post

# 1. Hammaning ruxsati bor (Read)
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/post_list.html', {'posts': posts})

# 2. Faqat Admin guruhidagilar (add_post permissioni borlar) uchun
@permission_required('posts.add_post', raise_exception=True)
def post_create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        # Normativda muallifni saqlash so'ralmagan bo'lsa ham, bu yaxshi amaliyot
        Post.objects.create(title=title, content=content)
        return redirect('post_list')
    return render(request, 'posts/post_form.html')

# 3. Faqat Admin guruhidagilar (change_post permissioni borlar) uchun
@permission_required('posts.change_post', raise_exception=True)
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('post_list')
    return render(request, 'posts/post_form.html', {'post': post})

# 4. Faqat Admin guruhidagilar (delete_post permissioni borlar) uchun
@permission_required('posts.delete_post', raise_exception=True)
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')