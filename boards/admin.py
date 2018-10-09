from django.contrib import admin

from accounts.models import User

from .models import Board, Topic

admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(User)
