from  django.views.generic import TemplateView
from django.urls import reverse
from django.shortcuts import redirect


class Redirect(TemplateView):
    def get(self, request, *args, **kwargs):
        return redirect(to=reverse('temp_home'))