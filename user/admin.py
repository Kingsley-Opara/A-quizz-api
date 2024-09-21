from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .forms import AdminChangeForm

User = get_user_model()

# Register your models here.

class UserAdmin(BaseUserAdmin):
    model = User
    search_fields = ['email']
    ordering = ['created']
    list_display = ['fullname', 'email']
    list_filter = ['is_superuser']

    form = AdminChangeForm

    fieldsets = (
        (None, {'fields': (['email'])}),
        ('Personal info', {'fields': ('fullname', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active', 'is_staff')}),
    )

    add_fieldsets = (
        (None, {
        'classes': ('wide',),
        'fields': ('email', 'fullname', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)
