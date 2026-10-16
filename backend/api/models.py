from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model): l


STATUS_CHOICES = (
    ('open', 'Open'),
    ('in_progress', 'In Progress'),
    ('closed', 'Closed'),
)

title = models.CharField(max_length=255)
description = models.TextField()
status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return self.title


class Reply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author.username} on {self.ticket.title}"
