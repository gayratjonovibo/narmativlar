from django.db import models

# 1-bosqich: BaseQuerySet
class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return self.update(is_deleted=True)


# 2-bosqich: DeletedManager
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        # Faqat o'chirilmaganlarni qaytarish
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)


# 3-bosqich: Post modeli
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()

    all_objects = models.Manager()

    def delete(self, *args, **kwargs):
        # Bitta obyekt uchun delete() override
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.title