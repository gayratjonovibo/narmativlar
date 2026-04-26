from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from accounts.decorators import my_login_required

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/post_list.html', {'posts': posts})

@my_login_required
def post_create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        Post.objects.create(title=title, content=content)
        return redirect('post_list')
    return render(request, 'posts/post_form.html')

@my_login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('post_list')
    return render(request, 'posts/post_form.html', {'post': post})

@my_login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')