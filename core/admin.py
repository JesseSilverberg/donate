from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from core.models import Donator

# Define an inline admin descriptor for Donator model
# which acts a bit like a singleton
class DonatorInline(admin.StackedInline):
    model = Donator
    can_delete = False
    verbose_name_plural = 'donator'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (DonatorInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)