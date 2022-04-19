from django.db import models,migrations
from django.contrib.auth.models import User
from django.utils.timezone import now

class Assignment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50,default ="")
    title = models.CharField(max_length= 100)
    description = models.TextField()
    due = models.DateTimeField(default=now)
    marks =models.IntegerField(default =None)
    pdffile = models.FileField(upload_to="assign/", max_length=250, null=True, default=None)
    

    def __str__(self):
        return self.title




