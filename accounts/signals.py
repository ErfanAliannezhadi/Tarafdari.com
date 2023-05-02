from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save
from django.core.files.storage import default_storage
from .models import UserModel


@receiver(pre_delete, sender=UserModel)
def user_delete(sender, **kwargs):
    instance = kwargs['instance']
    if instance.profile_image:
        default_storage.delete(instance.profile_image.name)
    if instance.cover_image:
        default_storage.delete(instance.cover_image.name)
    if instance.background_image:
        default_storage.delete(instance.background_image.name)


@receiver(post_save, sender=UserModel)
def user_update(sender, **kwargs):
    pass
