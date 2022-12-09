from django.db import models

class NippoModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
