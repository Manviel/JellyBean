from django.contrib import admin

from accounts.models import User

from .models import Board, Photo, Topic

admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(User)
admin.site.register(Photo)
