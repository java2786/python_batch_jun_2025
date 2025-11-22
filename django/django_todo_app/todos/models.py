from django.db import models

# Create your models here.
class Todo(models.Model):
    title=models.CharField(max_length=20)
    description=models.TextField(blank=True)
    completed= models.BooleanField(default=False)
    created_at=models.DateField(auto_now=True)
    updated_at=models.DateField(auto_now=True)
    
    def __str__(self):
        return f"[Title: {self.title}, Desc: {self.description}, Completed: {self.completed}]"