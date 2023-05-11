from django.forms import ModelForm, Textarea, Select, TextInput
from .models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'name': TextInput(attrs={'class': 'form-name', 'rows': 5, 'placeholder': 'Enter project name'}),
            'status': Select(attrs={'class': 'form-status', 'rows': 5}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter project description'}),
        }