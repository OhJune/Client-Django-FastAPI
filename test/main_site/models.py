from django.db import models

# Create your models here.
class board(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    
    def __str__(self):
        
        return self.subject

