from django.db import models

# Create your models here.

class Course(models.Model):
    MODE_CHOICES = [('online','Online'), ('offline','Offline'), ('hybrid','Hybrid')]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_weeks = models.PositiveIntegerField(default=4)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='online')
    certificate = models.BooleanField(default=True)
    mentors = models.CharField(max_length=255, blank=True, help_text="Comma-separated names")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title