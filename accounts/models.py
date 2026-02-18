from django.db import models
from django.db import models
from django.contrib.auth.models import User

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_active = models.DateTimeField(auto_now=True)
    session_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.last_active}"

class TrafficSource(models.Model):
    source_name = models.CharField(max_length=50)
    visits = models.IntegerField()

    def __str__(self):
        return self.source_name

class ActiveAuthor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contribution_score = models.IntegerField()
    role = models.CharField(max_length=50, default='Author')  # added role

    def __str__(self):
        return f"{self.user.username} - {self.contribution_score}"

class Designation(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"{self.title} at {self.company}"

class UserProfile(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    pan = models.CharField(max_length=20, blank=True)
    aadhar = models.CharField(max_length=20, blank=True)
    pan_card = models.FileField(upload_to='documents/pan/', blank=True, null=True)
    aadhar_card = models.FileField(upload_to='documents/aadhar/', blank=True, null=True)
    signature = models.FileField(upload_to='documents/signature/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"