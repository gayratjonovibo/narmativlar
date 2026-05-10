from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # ImageField rasm yuklash uchun
    image = models.ImageField(upload_to='posts/', null=True, blank=True)

    def __str__(self):
        return self.title