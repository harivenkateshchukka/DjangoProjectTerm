from django.db import models
from django.contrib.auth.models import User

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50, blank=False)

class BiometricDetails(models.Model):
    user = models.OneToOneField(UserDetails, on_delete=models.CASCADE)
    facial_scan = models.ImageField(upload_to='facial_scans/')

class Question(models.Model):
    pdf = models.FileField(upload_to='questions/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Submission(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_pdf = models.FileField(upload_to='answers/')
    submitted_at = models.DateTimeField(auto_now_add=True)

class Grade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE)
    score = models.IntegerField()
    feedback = models.TextField(blank=True)

class Active(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=50,unique=False,blank=False)
    ipaddress = models.CharField(max_length=50,blank=False)

    def str(self):
        return self.username

    class Meta:
        db_table = "ip_table"