from django.contrib import admin
from .models import MailMessage

@admin.register(MailMessage)
class MailMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('subject', 'body')
