from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_reader = models.BooleanField(default=False)
    is_blogger = models.BooleanField(default=False)


class Reader(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    actions = models.ManyToManyField(Action, through='Take')
    interests = models.ManyToManyField(Subject, related_name='interes_readers')
