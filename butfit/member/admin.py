from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User,Credit


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone', 'nickname','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('phone', 'nickname','password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'nickname','password1', 'password2')}
         ),
    )
    search_fields = ('phone','nickname')
    ordering = ('phone',)
    filter_horizontal = ()

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Credit)
