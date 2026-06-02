from django import forms
from django.contrib.auth.models import User
from .models import PasswordResetCode

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username kiriting'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Bunday username mavjud emas!")
        return username


class RestorePasswordForm(forms.Form):
    code = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '6 xonali kod'})
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Yangi parol'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni tasdiqlang'})
    )

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', "Parollar mos kelmadi!")

        if code:
            reset_code = PasswordResetCode.objects.filter(code=code, is_used=False).last()
            if not reset_code:
                self.add_error('code', "Kiritilgan kod noto'g'ri yoki allaqachon ishlatilgan!")
            elif reset_code.is_expired():
                self.add_error('code', "Kodning 2 daqiqalik vaqti tugabdi!")
            else:
                cleaned_data['reset_code_obj'] = reset_code

        return cleaned_data