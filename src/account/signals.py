import os

from django.db.models.signals import post_delete
from django.dispatch import receiver
from account.models import Avatar


@receiver(post_delete, sender=Avatar)
def user_post_delete(sender, instance, **kwargs):
    image_path = instance.file_path.path
    if os.path.exists(image_path):
        os.remove(image_path)
