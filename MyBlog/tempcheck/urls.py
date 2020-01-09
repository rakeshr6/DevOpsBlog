from django.conf import settings
from django.urls import path
from .views import *
from tempcheck import views
from django.conf.urls.static import static




urlpatterns = [

    path('', PostListView.as_view(), name='temp_home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='temp_post-detail'),
    path('user/<str:username>/', UserPostListView.as_view(), name='temp_user-posts'),
    path('post/new/', PostCreateView.as_view(), name='temp_post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='temp_post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='temp_post-delete'),


    path('comments/<int:pk_1>/post/<int:pk>/update/', CommentUpdateView.as_view(), name='temp_update_comment_to_post'),
    path('comments/post/<int:pk>/delete/', CommentDeleteView.as_view(), name='temp_delete_comment_to_post'),

    path('comment/<int:pk>/approve/', views.comment_approve, name='temp_comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='temp_comment_remove'),
    path('comment/reply/<int:pk>/approve/', views.reply_approve, name='temp_reply_approve'),
    path('comment/reply/<int:pk>/remove/', views.reply_remove, name='temp_reply_remove'),


    path('comment/<int:pk_1>/post/<int:pk>/replay/', ReplayCreateView.as_view(), name='temp_comment_replay'),
    path('comment/<int:pk_1>/post/<int:pk_2>/comment/<int:pk>/update/',
         ReplyUpdateView.as_view(), name='temp_replay_update'),
    path('comment/<int:pk>/delete/', ReplyDeleteView.as_view(), name='temp_replay_delete'),
    path('comment/<int:pk_1>/post/<int:pk>/replay/list/', ReplyListView.as_view(), name='temp_replay_list'),

    path('ajax/validate_username/', views.validate_username, name='validate_username'),
    path('ajax/comment_nofitication/', views.AjaxNotificationComment, name='ajax_notification_comment'),
    path('ajax/reply_nofitication/', views.AjaxNotificationReply, name='ajax_notification_reply'),

    path('likes/<int:pk>/', LikeAPIview.as_view(), name='api_post-like'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
