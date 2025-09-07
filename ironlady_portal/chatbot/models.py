from django.db import models

# Create your models here.

class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    # optional comma-separated keywords to assist matching
    keywords = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.question

class ChatMessage(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
