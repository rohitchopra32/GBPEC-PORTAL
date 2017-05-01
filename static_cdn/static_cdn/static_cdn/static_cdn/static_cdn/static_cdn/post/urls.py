from django.conf.urls import url
from django.contrib import admin

from .views import (
	post_home,
	post_update,
	post_detail,
	post_delete,
	post_create,
	)

urlpatterns = [
	url(r'^$', post_home, name='home'),
	url(r'^create/$', post_create),
	url(r'^(?P<id>\d+)/edit/$', post_update, name="update"),
	url(r'^(?P<id>\d+)/$', post_detail, name='detail'),
	url(r'^(?P<id>\d+)/delete/$',  post_delete, name='delete'),

]	 