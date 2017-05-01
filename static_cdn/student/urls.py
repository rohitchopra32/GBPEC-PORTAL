from django.conf.urls import url
from django.contrib import admin
from .views import (
	login_view,
	loggedin,
	
	)


urlpatterns = [
	url(r"^$", login_view ,  name="login"),
    #url(r"^accounts/loggedin/$", loggedin , name="loggedin"),
    url(r'^(?P<username>\w+)/$', loggedin, name='loggedin'),
    


]