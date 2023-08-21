from django.db import models

class ResultData(models.Model):
    output_data = models.TextField(blank=True, default="")
    
