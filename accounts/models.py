from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_reader = models.BooleanField(default=False)
    is_blogger = models.BooleanField(default=False)


class Subject(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span>%s</span>' % (color, name)
        return mark_safe(html)


class Choice(models.Model):
    description = models.CharField(max_length=30)

    def __str__(self):
        return self.description


class Reader(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    interests = models.ManyToManyField(Choice, related_name='interests')

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
