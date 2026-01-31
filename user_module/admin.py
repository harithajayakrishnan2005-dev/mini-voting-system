from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Poll, Option, Vote, Feedback, UserProfile

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'user_type')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'user_type', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(User, UserAdmin)

class OptionInline(admin.TabularInline):
    model = Option
    extra = 2

class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    inlines = [OptionInline]

admin.site.register(Poll, PollAdmin)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('poll', 'option', 'user')
    list_filter = ('poll', 'option', 'user')

admin.site.register(Vote, VoteAdmin)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'poll', 'rating_stars', 'comment', 'created_at')
    list_filter = ('poll', 'user', 'rating')
    search_fields = ('user__username', 'comment')

    def rating_stars(self, obj):
        if obj.rating:
            return "★" * obj.rating
        return "-"
    rating_stars.short_description = "Rating"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact', 'place', 'age')
