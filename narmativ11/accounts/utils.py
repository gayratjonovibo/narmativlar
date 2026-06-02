import threading
from django.core.mail import send_mail
from django.conf import settings

def send_email_in_thread(subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )

def thread_send_email(email, subject, message):
    thread = threading.Thread(
        target=send_email_in_thread,
        args=(subject, message, [email])
    )
    thread.start()