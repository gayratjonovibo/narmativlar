from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
        # Avvalgi normativdagi formlarni import qilamiz
from .forms import RegisterForm, LoginForm

from django.contrib.auth.models import Group  # Guruhlar bilan ishlash uchun


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # 7-normativ: User guruhini topamiz va yangi foydalanuvchiga biriktiramiz
            try:
                user_group = Group.objects.get(name='User')
                user.groups.add(user_group)
            except Group.DoesNotExist:
                # Agar guruh bazada hali yaratilmagan bo'lsa, xato bermasligi uchun
                pass

            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return redirect('post_list')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')