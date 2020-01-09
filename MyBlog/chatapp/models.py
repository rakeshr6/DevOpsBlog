from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    msg = models.CharField(max_length=102, null=True, blank=True)
    sendto = models.ForeignKey(User,on_delete=models.CASCADE, related_name='chatperson')
    sendfrom = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    msg_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.msg

    class Meta:
        ordering = ['msg_date']
