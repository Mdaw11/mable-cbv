from django.db import models
from users.models import CustomUser, Profile
from ckeditor.fields import RichTextField
from projects.models import Project

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    
    
class Ticket(models.Model):
    STATUS = (
        ('Open', 'Open'),
        ('Closed', 'Closed')
    )
    
    PRIORITIES = (
        ('None', 'None'),
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    )
    
    TYPE = (
        ('Misc', 'Misc'),
        ('Bug', 'Bug'),
        ('Help-Needed', 'Help-Needed'),
        ('Concern', 'Concern'),
        ('Question', 'Question')
    )
    
    host = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='host')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project')
    assignee = models.ManyToManyField(CustomUser, blank=True, related_name='assignee')
    name = models.CharField(max_length=200)
    status = models.TextField(choices=STATUS, default='Open', null=True)
    priority = models.TextField(choices=PRIORITIES, default='None', max_length=10)
    type = models.TextField(choices=TYPE, default='Misc', max_length=15)
    description = models.CharField(max_length=200, null=True, blank=True)
    # description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(CustomUser, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.name



class TicketHistory(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='history')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    status = models.TextField(choices=Ticket.STATUS, default='Open')
    priority = models.TextField(choices=Ticket.PRIORITIES, default='None', max_length=10)
    type = models.TextField(choices=Ticket.TYPE, default='Misc', max_length=15)
    description = RichTextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='attachments')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created']
    



class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.body[0:50]