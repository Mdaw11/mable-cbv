from django.test import TestCase, RequestFactory
from users.models import CustomUser
from django.urls import reverse
from .models import Notification
from tickets.models import Ticket
from . views import view_notifications, mark_notification_as_read
from .signals import create_ticket_notification, update_ticket_notification
from .context_processors import notifications

# Create your tests here.
class NotificationTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword')
        self.notification = Notification.objects.create(recipient=self.user, message='Test notification')

    def test_view_notifications(self):
        # Test that the view returns a 200 status code
        request = self.factory.get('/notifications/')
        request.user = self.user
        response = view_notifications(request)
        self.assertEqual(response.status_code, 200)

        # Test that the correct notifications are returned
        self.assertContains(response, self.notification.message)

        # Test that the notification is marked as read
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

        # Test that the count is correct
        self.assertContains(response, '1 unread notification')
    
    def test_mark_notification_as_read(self):
        # Test that the view returns a success JSON response
        request = self.factory.post(reverse('mark_notification_as_read', args=[self.notification.id]))
        request.user = self.user
        response = mark_notification_as_read(request, self.notification.id)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'success': True})

        # Test that the notification is marked as read
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
        
    def test_create_ticket_notification(self):
        # Test that a notification is created when a ticket is created
        create_ticket_notification(sender=Ticket, instance=self.ticket, created=True)
        notifications = Notification.objects.filter(recipient=self.user, ticket=self.ticket, notification_type='created')
        self.assertEqual(notifications.count(), 1)

    def test_update_ticket_notification(self):
        # Test that a notification is created when a ticket is updated
        update_ticket_notification(sender=Ticket, instance=self.ticket, created=False)
        notifications = Notification.objects.filter(recipient=self.user, ticket=self.ticket, notification_type='updated')
        self.assertEqual(notifications.count(), 1)
        
    def test_notifications_authenticated(self):
        # Test that notifications are returned for authenticated users
        request = self.factory.get('/')
        request.user = self.user
        response = notifications(request)
        self.assertEqual(len(response['notifications']), 1)
        self.assertEqual(response['count'], 1)

    def test_notifications_unauthenticated(self):
        # Test that no notifications are returned for unauthenticated users
        request = self.factory.get('/')
        request.user = CustomUser()
        response = notifications(request)
        self.assertEqual(len(response['notifications']), 0)
        self.assertEqual(response['count'], 0)
