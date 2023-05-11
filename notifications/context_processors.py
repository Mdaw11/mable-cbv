from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user, is_read=False).select_related('ticket')
        count = notifications.count()
    else:
        notifications = []
        count = 0
    return {'notifications': notifications, 'count': count}