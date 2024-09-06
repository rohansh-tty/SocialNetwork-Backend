from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    avatar = models.URLField(null=True, blank=True)
    friends = models.ManyToManyField('self', blank=True)
    class Meta:
        indexes = [
            models.Index(fields=['email', 'name']),
        ]
    
    def __str__(self):
        return f'{self.name} - {self.email}'
 
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests', to_field='email')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests', to_field='email')
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        unique_together = ('sender', 'receiver')
        
    def __str__(self):
        return f"{self.sender.name} - {self.receiver.name} ({self.status})"