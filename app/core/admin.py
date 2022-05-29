from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # noqa
from django.contrib.auth import get_user_model


# Register your models here.
class UserAdmin(UserAdmin):
    """
    Custom user admin
    """
    list_display = ('email', 'name', 'phone_number', 'language', 'currency', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'phone_number', 'language', 'currency')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'name', 'phone_number', 'language', 'currency',
                'password1', 'password2', 'is_staff', 'is_active'
            )
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(get_user_model(), UserAdmin)
