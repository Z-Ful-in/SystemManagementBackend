from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserImage(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')  # 图片会上传到 MEDIA_ROOT/images/
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description