import logging
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Task

logger = logging.getLogger(__name__)


# 📌 Background Task (View ichida .delay() bilan chaqiriladi)
@shared_task
def send_post_creation_log(post_id, title):
    """
    Post yaratilganda orqa fonda (background) ishlaydigan task.
    """
    logger.info(f"🟢 [BACKGROUND TASK] Yangi post yaratildi! ID: {post_id}, Title: {title}")
    return f"Post ID {post_id} uchun log yozildi."


# 📌 Periodik Task (Celery Beat har 1 minutda ishlatadi)
@shared_task
def check_old_posts_task():
    """
    Har 1 minutda eski postlarni (masalan, 1 kundan eski) tekshiruvchi task.
    """
    one_day_ago = timezone.now() - timedelta(days=1)
    old_posts_count = Task.objects.filter(created_at__lt=one_day_ago).count()

    logger.info(f"⏰ [CELERY BEAT] Periodik tekshiruv: 24 soatdan eski postlar soni: {old_posts_count} ta")
    return f"{old_posts_count} ta eski post tekshirildi."