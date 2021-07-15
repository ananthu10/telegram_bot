from django.db import models

# Create your models here.
class UserLogger(models.Model):
    userId=models.IntegerField()
    userName=models.CharField(max_length=30,primary_key=True)
    fat=models.IntegerField(default=0)
    stupid=models.IntegerField(default=0)
    dumb=models.IntegerField(default=0)
    created=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.userName