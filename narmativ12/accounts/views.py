from django.shortcuts import render
from django.utils.translation import gettext as _


def home_view(request):
    welcome_message = _("Welcome to our booking application!")

    context = {
        'welcome_message': welcome_message
    }
    return render(request, 'accounts/home.html', context)