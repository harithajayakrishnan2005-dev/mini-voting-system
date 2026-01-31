from django.contrib import admin
from user_module.models import Poll, Option, Feedback, Vote

class OptionInline(admin.TabularInline):
    model = Option
    extra = 2

class PollAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

admin.site.register(Option)

from django.contrib import admin
from user_module.models import Vote

class VoteAdmin(admin.ModelAdmin):
    list_display = ('poll', 'option', 'user', 'voted_at')  
    list_filter = ('poll', 'option', 'user', 'voted_at')
    
