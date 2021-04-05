from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserProfile
 
 
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'organization', 'email', 'phone', 'address', 'is_staff')


admin.site.register(UserProfile, UserProfileAdmin)
#admin.site.unregister(User)