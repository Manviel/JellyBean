from django.contrib import admin

from accounts.models import User

from .models import Board, Photo, Topic


def apply_active(modeladmin, request, queryset):
    for board in queryset:
        board.description = ''
        board.save()


apply_active.short_description = 'Apply'


class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    actions = [apply_active, ]

    def get_model_perms(self, request):
        return {}


admin.site.register(Board, BookAdmin)
admin.site.register(Topic)
admin.site.register(User)
admin.site.register(Photo)
