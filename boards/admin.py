from django.contrib import admin

from accounts.models import Subject, User

from .models import Board, Topic

admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(User)
admin.site.register(Subject)
