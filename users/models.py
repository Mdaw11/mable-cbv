from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
# Create your models here.

class CustomUser(AbstractUser):
    ACCOUNT_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('developer', 'Developer'),
        ('project_manager', 'Project Manager')
    )
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=CustomUser.ACCOUNT_TYPE_CHOICES)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)
    

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()