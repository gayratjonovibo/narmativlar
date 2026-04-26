from django.shortcuts import redirect

def my_login_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login') # Login qilmagan bo'lsa, haydaymiz
        return func(request, *args, **kwargs)
    return wrapper