from users.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from tickets.models import Ticket
from notifications.models import Notification

@receiver(post_save, sender=Ticket)
def create_ticket_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(recipient=instance.host, ticket=instance, message='Your ticket has been created', notification_type='created')
        
        
@receiver(post_save, sender=Ticket)
def update_ticket_notification(sender, instance, created, **kwargs):
    if not created:
        Notification.objects.create(recipient=instance.host, ticket=instance, message='Your ticket has been updated', notification_type='updated')