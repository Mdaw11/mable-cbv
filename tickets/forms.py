from django.forms import ModelForm, Textarea, Select, TextInput
from .models import Ticket
from django import forms
from ckeditor.widgets import CKEditorWidget
from users.models import CustomUser

class TicketForm(ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    assignees = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-assignees'}),
    )

    class Meta:
        model = Ticket
        exclude = ['host', 'category', 'participants']
        widgets = {
            'name': TextInput(attrs={'class': 'form-name custom-input', 'placeholder': 'Enter ticket name'}),
            'project': Select(attrs={'class': 'form-project', 'rows': 5}),
            'status': Select(attrs={'class': 'form-status', 'rows': 5}),
            'priority': Select(attrs={'class': 'form-priority', 'rows': 5}),
            'type': Select(attrs={'class': 'form-type', 'rows': 5}),
        }