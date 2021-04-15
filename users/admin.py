from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'organization', 'email', 'phone', 'address', 'is_staff'
    )


admin.site.register(UserProfile, UserProfileAdmin)
# admin.site.unregister(User)
