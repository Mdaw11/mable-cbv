from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Notification

# Create your views here.
def view_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user, read=False)
    count = notifications.filter(is_read=False).count()

    for notification in notifications:
        if not notification.is_read:
            notification.is_read = True
            notification.save()
    

    context = {'notifications': notifications, 'count': count}
    return render(request, 'navbar.html', context)

def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.is_read = True
    notification.save()
    response_data = {'success': True}
    return JsonResponse(response_data)