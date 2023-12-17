from django.contrib import admin

from mailing.models import Client, Mailing


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('FIO', 'email', 'comment', )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'finish_time', 'send_frequency', 'mailing_status',)
    list_filter = ('mailing_status',)
    search_fields = ('mailing_status',)
