import os
from django.utils import timezone
from django.conf import settings


class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file_path = os.path.join(settings.BASE_DIR, 'requests.log')

    def __call__(self, request):
        time_str = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        path = request.path
        ip_address = request.META.get('REMOTE_ADDR', 'Unknown IP')

        if request.user and request.user.is_authenticated:
            username = request.user.username
        else:
            username = "AnonymousUser"

        log_entry = f"[{time_str}] User: {username} IP: {ip_address} Path: {path}\n"

        with open(self.log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        response = self.get_response(request)
        return response