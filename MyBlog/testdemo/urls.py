from django.urls import path
from .views import *

urlpatterns = [

    path('', index, name='index'),
    # path('create', CreateViewPage.as_view(), name='create'),

]