import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


def user_avatar_upload(instance, filename):
    return f'{instance.user_id}/{filename}'


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(
        'email address', blank=False, null=False, unique=True
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.username = str(uuid.uuid4())
        super().save(*args, **kwargs)

    @property
    def get_avatar_url(self):
        avatar = self.avatar_set.get(active_avatar=True)
        image_url = avatar.file_path.url
        return image_url

    class Meta:
        permissions = [
            ("full_edit", "full edit")
        ]


choice = ((1, 1,),)


class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_path = models.FileField(upload_to=user_avatar_upload)
    active_avatar = models.BooleanField(null=True)

    class Meta:
        unique_together = ('user', 'active_avatar',)
