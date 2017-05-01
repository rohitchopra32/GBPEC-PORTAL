from django.shortcuts import render
from django.template.context_processors import csrf
from  django.http import HttpResponseRedirect, HttpResponse
from  django.shortcuts import render_to_response
from django.urls import reverse


from .models import student
from .forms import loginForm

# Create your views here.


def login(request):
	c = {}
	c.update(csrf(request))
	return render(request, "login.html", c)

def auth_view(request):
	roll_no = request.POST.get("username", "")
	password = request.POST.get("password", "")

	q = student.objects.get(roll_no=roll_no)

	if q.password==password:
		return  HttpResponseRedirect("/student/%s/"%(q.name))

	return  HttpResponseRedirect("/studemt/accounts/invalid")



def loggedin(request, username):
	return  render(request, "loggedin.html", {"full_name": username})


def invalid(request):
    return  render(request, "invalid_login.html")


def logout(request):
    return  render(request, "logout.html")