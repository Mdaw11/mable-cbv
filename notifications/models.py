from django.db import models
from users.models import CustomUser
from tickets.models import Ticket

# Create your models here.
class Notification(models.Model):
    OPTIONS = (
        ('created', 'created'),
        ('updated', 'updated'),
    )
    
    recipient = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='notifications')
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(choices=OPTIONS, max_length=15, null=True)
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)