"""GBPEC_PORTAL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView


# from ajax_select import urls as ajax_select_urls
from classroom.views import classroom_full, classroom_create, search, profile, edit_profile, post_full, post_edit, post_delete, create_user, file_delete, changepassword
from student.views import (
    login_view,
    
    )
from fourms.views import forumView, editForum, deleteForum, fullForum, deletePost, editPost


urlpatterns = [
    url(r'^messages/', include('postman.urls', namespace='postman', app_name='postman')),
    url(r'^admin/', admin.site.urls),
    url(r"^$", login_view ,  name="login"),
    url(r'^logout/$', views.logout,{'next_page': '/'}),
    url(r'^comments/', include("comments.urls", namespace='comments')),
    url(r'^createuser/$', create_user, name='create_user'),
    url(r'^createuser/$', create_user, name='create_user'),
    # url(r'^messages/', include('django_messages.urls')),
    # url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^(?P<username>\w+)/profile/$', profile, name='profile'),
    url(r'^(?P<username>\w+)/edit_profile/$', edit_profile, name='edit_profile'),
    url(r'^(?P<username>\w+)/edit_profile/changepassword/$', changepassword, name='changepassword'),
    url(r'^(?P<username>\w+)/forum/(?P<sortby>[\w-]+)/$', forumView, name='forumsortView'),
    url(r'^(?P<username>\w+)/forum/$', forumView, name='forumView'),
    url(r'^(?P<username>\w+)/forumfull/(?P<slug>[\w-]+)/$', fullForum, name='fullForum'),
    url(r'^(?P<username>\w+)/forum/(?P<slug>[\w-]+)/edit/$', editForum, name='editForum'),
    url(r'^(?P<username>\w+)/forum/(?P<slug>[\w-]+)/delete/$', deleteForum, name='deleteForum'),
    url(r'^(?P<username>\w+)/forum/post/(?P<slug>[\w-]+)/edit/$', editPost, name='editPost'),
    url(r'^(?P<username>\w+)/forum/post/(?P<slug>[\w-]+)/delete/$', editPost, name='deletePost'),
    url(r'^(?P<username>\w+)/post/(?P<slug>[\w-]+)/$', post_full, name='post_full'),
    url(r'^(?P<username>\w+)/post/(?P<slug>[\w-]+)/edit/$', post_edit, name='post_edit'),
    url(r'^(?P<username>\w+)/post/(?P<slug>[\w-]+)/delete/$', post_delete, name='post_delete'),
    url(r'^search/(?P<query>[\w-]+)/$', search, name='search'),
    url(r'^(?P<username>\w+)/(?P<slug>[\w-]+)/$', classroom_full, name='classroom_full'),
    url(r'^(?P<username>\w+)/$', classroom_create, name='classroom_create'),
    url(r'^(?P<username>\w+)/(?P<slug>[\w-]+)/(?P<file_name>[\w_]+[\w-]+.[\w]+)/delete/$', file_delete, name='file_delete'),


    # url(r'^post/comments/', include('fluent_comments.urls')),
    

    
    
    
    

    

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)