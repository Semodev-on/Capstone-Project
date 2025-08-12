from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    POSITION_CHOICES = [
        ('teacher', 'Teacher'),
        ('subject_coordinator', 'Subject Coordinator'),
        ('principal', 'Principal'),
    ]
    
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, default='teacher')
    institutional_school = models.CharField(max_length=255, verbose_name="Institutional (School)")
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_position_display()}"
