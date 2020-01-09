from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from activity_log.models import ActivityLog


class ActivityLogView(LoginRequiredMixin, ListView):
    model = ActivityLog
    template_name = 'activity_log/activity_log_view.html'
    context_object_name = 'activity'
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['activity'] = self.model.objects.filter(user=self.request.user)
        return context
