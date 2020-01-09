from django.urls import path
from activity_log import views
from .views import ActivityLogView
from django.conf.urls import url


urlpatterns= [

    url(r'^log/$', ActivityLogView.as_view(), name='activity_log')
]