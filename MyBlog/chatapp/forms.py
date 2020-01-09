from django import forms
from chatapp.models import *

class ChatForm(forms.ModelForm):
    class Meta:
        model =Chat
        fields = ['msg']
        widgets = {
            'msg': forms.Textarea(attrs={'cols': 50, 'rows': 2},

          )
        }
