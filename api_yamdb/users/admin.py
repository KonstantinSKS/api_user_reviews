from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'role',
        'email',
        'first_name',
        'last_name',
        'bio'
    )
    empty_value_display = '-пусто-'
