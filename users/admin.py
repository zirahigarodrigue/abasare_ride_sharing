from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password')
        }),
        ('Personal Information', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name')
        }),
        ('Permissions', {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'classes': ('collapse',),
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        ('REGISTER NEW USER', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name','email',('is_vehicle_owner','is_umusare_rider'),'password1','password2',),
        }),
    )

admin.site.register(UserAccount, CustomUserAdmin)
