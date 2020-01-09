from django.contrib import admin

from tempcheck.models import Post, Comment, CommentReplay

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(CommentReplay)

