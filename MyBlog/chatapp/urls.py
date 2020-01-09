from django.urls import path
from .views import *
from chatapp import views

urlpatterns = [
    path('usermessagelist/', UserMessageListView.as_view(), name='user_msg_list'),
    # path('messagelist/<int:pk>/', MessageDetailView.as_view(), name='msg_list'),
    path('ajax/chat/', views.chatajaxview, name = "ajax_chat")

    ]
