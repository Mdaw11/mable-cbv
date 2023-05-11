import django_filters
from django.forms import ModelForm, Textarea, Select, TextInput, SelectMultiple
from .models import Ticket
from users.models import CustomUser

class TicketFilter(django_filters.FilterSet):
    assignee = django_filters.ModelMultipleChoiceFilter(
        queryset=CustomUser.objects.all().order_by('username'),
        widget=Select(attrs={'class': 'assignee-dropdown'})
    )
    status = django_filters.ChoiceFilter(
        choices=Ticket.STATUS,
        widget=Select(attrs={'class': 'status-dropdown'})
    )
    priority = django_filters.ChoiceFilter(
        choices=Ticket.PRIORITIES,
        widget=Select(attrs={'class': 'priority-dropdown'})
    )
    type = django_filters.ChoiceFilter(
        choices=Ticket.TYPE,
        widget=Select(attrs={'class': 'type-dropdown'})
    )
    
    class Meta:
        model = Ticket
        fields = ['assignee', 'status', 'priority', 'type']