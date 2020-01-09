from django import forms
from django.forms import Textarea

from .models import Post, Comment, CommentReplay


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'img']
        labels = {
            'img': 'Image'
        }
        get_latest_by = '-date_posted'


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text', ]
        labels = {
            'text': 'Add Your Comment'
        }
        widgets = {
            'text': Textarea(attrs={'cols': 90, 'rows': 4}),
        }
        get_latest_by = '-created_date'


class ReplayForm(forms.ModelForm):

    class Meta:
        model = CommentReplay
        fields = ['Replay']
        labels ={
            'Replay': 'Reply'
        }
        widgets = {
            'Replay': Textarea(attrs={'cols': 30, 'rows': 3}),
        }
