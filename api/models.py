from django.db import models
from django.contrib.auth.models import User

class ToDosn(models.Model):

    Task_name=models.CharField(max_length=200)
    User= models.ForeignKey(User,on_delete=models.CASCADE)
    Status= models.BooleanField(default=False)
    Created_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Task_name

