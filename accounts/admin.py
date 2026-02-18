from django.contrib import admin
from .models import TrafficSource, ActiveAuthor, Designation, UserActivity, UserProfile

@admin.register(TrafficSource)
class TrafficSourceAdmin(admin.ModelAdmin):
    list_display = ('source_name', 'visits')

@admin.register(ActiveAuthor)
class ActiveAuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'contribution_score')

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'date')

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_active', 'session_count')

# Register UserProfile using the older style to avoid any conflict
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'status')

admin.site.register(UserProfile, UserProfileAdmin)