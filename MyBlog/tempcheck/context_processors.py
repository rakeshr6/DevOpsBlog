from django.shortcuts import get_object_or_404

from .models import Post, Comment, CommentReplay




def post_count(request):
    count = Post.objects.count()
    return {'post_count': count}

def notifi_count(request):
    coun = Post.objects.count()
    from django.contrib.auth.models import User
    if request.user.is_anonymous:
        pass

    else:
        comment_count = Comment.objects.filter(comment_notifi=False, post__author=request.user).values('post').distinct().count()
        comment = Comment.objects.filter(comment_notifi=False, post__author=request.user).values('post', 'post__title', 'text', 'author__username', 'id').distinct()
        comment_reply = CommentReplay.objects.filter(reply_notifi=False).values('post').count()
        requesting_user = CommentReplay.objects.filter(reply_notifi=False, author=request.user).count()
        comment_reply_count = comment_reply - requesting_user
        notification_count = comment_count + comment_reply_count
        reply_comment = CommentReplay.objects.filter(reply_notifi=False).exclude(author=request.user)
        return {'notification_count': notification_count, 'comment_in_post': comment, 'reply_comment':reply_comment}
    return {'post1_count': coun}