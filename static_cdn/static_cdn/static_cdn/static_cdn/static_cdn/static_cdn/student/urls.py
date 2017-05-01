from django.conf.urls import url
from django.contrib import admin
from .views import (
	login,
	auth_view,
	loggedin,
	logout
	)


urlpatterns = [
	url(r"^$", login ,  name="login"),
    url(r"^accounts/auth/$", auth_view ,name="auth_view"),
    #url(r"^accounts/loggedin/$", loggedin , name="loggedin"),
    url(r"^accounts/logout/$", logout, name="logout"),
    url(r'^(?P<username>\w+)/$', loggedin, name='loggedin'),


]