from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=False, null=False)
    datetime = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=1000)
    isAnswered = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name