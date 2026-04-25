from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    role = 'admin' if instance.is_superuser or instance.is_staff else 'customer'
    UserProfile.objects.create(user=instance, role=role)