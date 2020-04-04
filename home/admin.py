from django.contrib import admin
from .models import Setting, ContactFormMessage


class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status']
    list_filter = ['status']
    list_editable = ['status']


admin.site.register(Setting)
admin.site.register(ContactFormMessage, ContactFormMessageAdmin)
