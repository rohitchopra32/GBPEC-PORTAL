from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

    )

from django.shortcuts import render, get_object_or_404
from django.template.context_processors import csrf
from  django.http import HttpResponseRedirect, HttpResponse
from  django.shortcuts import render_to_response
from django.urls import reverse
from django.contrib.auth.models import Group, User

from .models import student
from .forms import UserLoginForm

# Create your views here.


def login_view(request):
	title = "Login"
	form = UserLoginForm(request.POST or None)
	print(form)
	if form.is_valid():
	    username = form.cleaned_data.get("username")
	    password = form.cleaned_data.get('password')
	    user = authenticate(username=username, password=password)
	    login(request, user)
	    return HttpResponseRedirect("%s/"%(request.user.username))


	return render(request, "login.html", {"form":form, "title": title})


# def profile(request, username=None):
# 	s = student.objects.filter(roll_no = username)
# 	s1 = student.objects.filter(roll_no = username).values('classroom')
# 	context = {"username": username, "profile":s}
# 	print(s1)
# 	clas = Classroom.objects.filter()
# 	instance = student.objects.get(roll_no = username)
# 	if instance.first == True:
# 		context.update({"notice":"Edit Your Profile Immediately"})

# 	print(context)
# 	return  render(request, "profile.html", context )

def logout_view(request):
    logout(request)
    return redirect("/")



