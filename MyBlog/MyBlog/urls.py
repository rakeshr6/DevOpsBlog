"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include, re_path
from users import views as user_views
from django.contrib.auth import views as auth_views
from .views import Redirect
from users.views import ForgotPasswordView, ResetPasswordView


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', Redirect.as_view(), name='redirect'),
    path('checktemp/', include('tempcheck.urls')),
    path('testdemo/', include('testdemo.urls')),
    path('blogapi/', include('blog_api.urls')),
    path('chatapp/', include('chatapp.urls')),
    path('activity/', include('activity_log.urls')),

    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    re_path('forget-password/', ForgotPasswordView.as_view(), name='forget_password'),
    re_path('reset-password/', ResetPasswordView.as_view(), name='reset_password')


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)