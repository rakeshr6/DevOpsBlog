from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(default='default.jpeg', upload_to='post_pics')
    likes = models.ManyToManyField(User, related_name='likes', default=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    draft = models.BooleanField(default=False)
    date_posted = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('temp_user-posts', kwargs={'username': self.author})

    def get_like_api_url(self):
        return reverse('api_post-like', kwargs={'pk': self.pk})

    @property
    def approved_comments(self):
        return self.comments.filter(approved_comment=True).count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=120)
    created_date = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)
    comment_notifi = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_replay(self):
        return CommentReplay.objects.filter(comment=self)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('temp_post-detail', kwargs={'pk': self.post.pk})


    def viewed_comment(self):
        self.comment_notifi = True
        self.save()


class CommentReplay(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_replay')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    Replay = models.TextField(max_length=120)
    created_date = models.DateTimeField(auto_now_add=True)
    approved_replay = models.BooleanField(default=False)
    reply_notifi = models.BooleanField(default=False)

    def __str__(self):
        return self.Replay

    def approve(self):
        self.approved_replay = True
        self.save()

    def get_absolute_url(self):
        return reverse('temp_post-detail', kwargs={'pk': self.post.pk})



