from django.db import models

User_Type_CHOICES = (
    ("1", "Interviewee"),
    ("2", "Interviewer"),
)

# Create your models here.
class User_Info(models.Model):
    user_Type = models.CharField(max_length=200,choices = User_Type_CHOICES,default = '1')
    full_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=254, blank=False)
    def __str__(self):
        return self.full_name

class Interview_Info(models.Model):
    startTime = models.DateTimeField(blank=False, null=True)
    endTime = models.DateTimeField(blank=False, null=True)
    participants = models.ManyToManyField(User_Info)

    def __str__(self):
        return str(self.id)
