from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Tutore, User


@receiver(post_save, sender=User)
def create_or_update_tutore(sender, instance, created, **kwargs):
    if created:
        tutore = Tutore(user=instance,
                              nr_pacienti=0)
        print('!!!!!!!!!!!!!!!!!!!!!' * 10)
        tutore.save()

