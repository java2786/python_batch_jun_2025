from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    

    # /tasks/{self.pk}/
    def get_absolute_url(self):
        # Mapping View Names to URLs
        # the reverse function in Django does not reverse a string or change the order of characters
        return reverse('task_detail', kwargs={'pk': self.pk})
