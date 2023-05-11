from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.view_notifications, name='view_notifications'),
    path('mark_notification_as_read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
]