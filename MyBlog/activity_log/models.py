from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_user')
    activity = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "user:{} activity : {}".format(self.user, self.activity)

    class Meta:
        ordering = ['-datetime']

