from django.db import models
from django.conf import settings
from users.models import CustomUser

# Create your models here.
class Project(models.Model):
    STATUS = (
        ('None', 'None'),
        ('In-Progress', 'In-Progress'),
        ('Under-Review', 'Under-Review'),
        ('Done', 'Done'),
    )
    
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='user')
    status = models.TextField(choices=STATUS, default="None")
    assigned_users = models.ManyToManyField(CustomUser, related_name="assigned_users", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.name