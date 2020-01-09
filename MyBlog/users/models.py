from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pic')
    about = models.CharField(max_length=100, default='About Author Details')

    def __str__(self):
        return '%s Profile' % self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class UserOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=100)
    isvalid = models.BooleanField(default=True)
    datetime = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "{}-User:{}-Date:{}".format(self.otp, self.user.username, self.datetime)