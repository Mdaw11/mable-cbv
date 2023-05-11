from django.contrib import admin

# Register your models here.

from .models import Category, Ticket, Message, TicketHistory, Attachment

admin.site.register(Category)
admin.site.register(Ticket)
admin.site.register(Message)
admin.site.register(TicketHistory)
admin.site.register(Attachment)