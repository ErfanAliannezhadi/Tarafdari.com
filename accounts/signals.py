from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save
from django.core.files.storage import default_storage
from .models import UserModel, EmojiPackageModel


@receiver(pre_delete, sender=UserModel)
def user_delete(sender, **kwargs):
    """
    Removes each user's images from storage just before deleting the user from the database
    """
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


@receiver(post_save, sender=UserModel)
def create_emoji_user(sender, **kwargs):
    """
    creates a row in database for every two distinct user for emoji package table
    default values will be False
    """
    instance = kwargs['instance']
    if kwargs['created']:
        # after user creation, we will make emoji packages for it
        for user in UserModel.objects.all():
            EmojiPackageModel.objects.update_or_create(from_user=instance, to_user=user)
            EmojiPackageModel.objects.update_or_create(from_user=user, to_user=instance)
    else:
        # after a user page become public, every follow request will accept
        if instance.is_private is False:
            for item in instance.other_follow_requests.all():
                item.accept()
