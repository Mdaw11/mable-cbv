from django.urls import path
from . import views 
from .views import HomeView, AnalyticsView, TicketHomeView, TicketView, UpdateTicketView, TicketDeleteView, DeleteMessageView

urlpatterns = [
    path('dashboard/', HomeView.as_view(), name='home'),
    path('tickets/', TicketHomeView.as_view(), name='ticket-home'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    
    path('ticket_data/', views.get_ticket_data, name='ticket-data'),
    path('type_data/', views.get_type_data, name='type-data'),
    path('status_data/', views.get_status_data, name='status-data'),

    path('ticket/<int:pk>', TicketView.as_view(), name='ticket'),
    path('update-ticket/<int:pk>/', UpdateTicketView.as_view(), name='update-ticket'),
    path('delete-ticket/<int:pk>/', TicketDeleteView.as_view(), name='delete-ticket'),
    path('delete-message/<int:pk>/', DeleteMessageView.as_view(), name='delete-message'),
    
    
    path('categories/', views.categoriesPage, name='categories'),
    path('activity/', views.activityPage, name='activity'),
]