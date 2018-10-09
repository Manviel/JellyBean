from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_reader = models.BooleanField(default=False)
    is_blogger = models.BooleanField(default=False)


class Subject(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Reader(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    interests = models.ManyToManyField(Subject, related_name='interests')

    def __str__(self):
        return self.user.username


class Blogger(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    birth = models.DateTimeField(
        auto_now=False,
        null=True
    )
    hobbies = models.ManyToManyField(Subject, related_name='hobbies')

    def __str__(self):
        return self.user.username
