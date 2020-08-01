from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
# class Donator(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     link = models.CharField(max_length=100)
#
#     tickets = models.IntegerField(validators=[MaxValueValidator(12), MinValueValidator(1)])


class Donator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)

    # first_name = models.CharField(max_length=100, blank=True)
    # last_name = models.CharField(max_length=100, blank=True)
    # email = models.EmailField(max_length=150)
    # bio = models.TextField()
    # link = models.CharField(max_length=100)
    # tickets = models.IntegerField(validators=[MaxValueValidator(12), MinValueValidator(1)])

    def __str__(self):
        return self.user.username


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Donator.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.donator.save()

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Donator.objects.create(user=instance)
    instance.donator.save()
