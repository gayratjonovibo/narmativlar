from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ForgotPasswordForm, RestorePasswordForm
from .models import PasswordResetCode
from .utils import thread_send_email


class ForgotPasswordView(View):

    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, 'accounts/forgot_password.html', {'form': form})

    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)

            reset_code = PasswordResetCode.objects.create(user=user)

            subject = "Parolni tiklash"
            message = f"Code: {reset_code.code}"

            if user.email:
                thread_send_email(user.email, subject, message)
                messages.success(request, "Emailingizga tasdiqlash kodi yuborildi!")
                return redirect('restore_password')
            else:
                form.add_error(None, "Foydalanuvchining email manzili kiritilmagan!")

        return render(request, 'accounts/forgot_password.html', {'form': form})


class RestorePasswordView(View):
    def get(self, request):
        form = RestorePasswordForm()
        return render(request, 'accounts/restore_password.html', {'form': form})

    def post(self, request):
        form = RestorePasswordForm(request.POST)
        if form.is_valid():
            reset_code = form.cleaned_data.get('reset_code_obj')
            user = reset_code.user
            new_password = form.cleaned_data.get('new_password')

            # 6-bosqich: Parolni yangilash
            user.set_password(new_password)
            user.save()

            # Kod qayta ishlatilmasligi uchun yopiladi
            reset_code.is_used = True
            reset_code.save()

            messages.success(request, "Parolingiz muvaffaqiyatli yangilandi!")
            return redirect('login')

        return render(request, 'accounts/restore_password.html', {'form': form})