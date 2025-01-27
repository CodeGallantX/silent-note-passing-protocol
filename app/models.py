from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_notes")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_notes")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note from {self.sender} to {self.receiver} - {self.subject}"
