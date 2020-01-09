from  django.urls import include, path, re_path
from blog_api import views
from rest_framework import routers
from blog_api.views import PostListApiView, PostDetailApiView, PostDeleteApiView, PostcreateApiView, PostUpdateApiView,\
    CreateUserApiView, UserLoginApiView

router = routers.DefaultRouter()

router.register(r'users', views.UserViewset)

urlpatterns = [
    path('api/', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    # re_path('api/loginview/', UserApiView.as_view(), name='user_api_view'),
    re_path(r'api/create/$', PostcreateApiView.as_view(), name='post_create_api_view'),
    re_path(r'api/update/(?P<pk>\d+)$', PostUpdateApiView.as_view(), name='post_update_api_view'),
    re_path(r'api/postlist/$', PostListApiView.as_view(), name='post_api_view'),
    re_path(r'api/postlist/(?P<pk>\d+)/$', PostDetailApiView.as_view(), name='post_detail_api_view'),
    re_path(r'api/postlist/(?P<pk>\d+)/delete/$', PostDeleteApiView.as_view(), name='post_delete_api_view'),
    re_path(r'api/create_user/$', CreateUserApiView.as_view(), name='create_user_view'),
    re_path(r'api/login_user/$', UserLoginApiView.as_view(), name='login_user_view'),
]