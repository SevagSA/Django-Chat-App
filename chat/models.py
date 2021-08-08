from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
    room_name = models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    newest_message = models.OneToOneField(
        'Message', on_delete=models.CASCADE, blank=True, null=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=400)
    message_media = models.ImageField(
        upload_to='message_media', null=True, blank=True)

    def __str__(self):
        return self.message[:30] + ('...' if len(self.message) > 30 else '')
