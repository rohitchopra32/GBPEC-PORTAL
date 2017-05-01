from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType

from django.contrib import messages
from django.db.models import Q
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

import uuid
import random
# Create your views here.
from .models import Classroom, background, create_slug as cs 
from .forms import classroomForm
from student.models import student
from teacher.models import teacher
from posts.models import create_slug, file, classPost as Post
from posts.forms import PostForm, StudentPostForm, FileForm
from teacher.forms import TeacherProfileForm
from student.forms import StudentProfileForm
from background.models import Background
from .utils import write
from comments.forms import CommentForm
from comments.models import Comment
from fourms.models import category, Fourms, forumPost


@login_required
def classroom_create(request, username = None):
	if not request.user.is_authenticated:
		raise Http404
	group_id = User.objects.filter(username = request.user.username).values('groups')
	group = str(Group.objects.get(id = group_id))
	form = None
	context = {"form":form, "username " :username,}
	
	if 'teacher' in group :
		t = teacher.objects.get_or_create(first_name = request.user.first_name, last_name = request.user.last_name, username = request.user, email = request.user.email )
		queryset = teacher.objects.values_list('position',flat=True).get(username=request.user)
		print(queryset)
		classrooms = Classroom.objects.filter(teacher = request.user)
		form = classroomForm(request.POST or None)
		context.update({'form':form,"group":True, "class":classrooms})
		if str(queryset).strip()=='Principal' or str(queryset).strip()=='dean':
			all_c=Classroom.objects.filter()
			print(all_c)
			context.update({"class":all_c})
		if form.is_valid():
			instance = form.save(commit=False)
			if Classroom.objects.filter(name = instance.name).exists():
				print(classrooms)
			else:
				instance.teacher = request.user	
				instance.background= background()
				code = str(uuid.uuid4())
				print(instance)
				instance.code = code[:4]
				slug = cs(instance)
				instance.slug = slug
				instance.save()
				print(instance.teacher)
				messages.success(request, 'classroom added successfully <br> <h4>%s</h4>Classroom Code'%instance.code, extra_tags='html_safe')
			return HttpResponseRedirect('/%s/'%request.user.username)
		# else:
		#  	messages.warning(request, 'Classroom already present')
		#  	# return HttpResponseRedirect('/%s/'%request.user.username)

	if 'student' in group :
		# s = student.objects.get_or_create(roll_no = username, first_name = request.user.first_name, last_name = request.user.last_name, email = request.user.email)
		c = student.objects.get(username=request.user)
		c1 = student.objects.filter(username = request.user).values('classroom')
		
		l=[]
		try:
			for j in c1:
				l.append(int(j['classroom']))
		except:
			messages.warning(request, 'no classroom')	
		cl = Classroom.objects.filter(pk__in=l)
		
		
		context.update({"group":False, 'classroom':cl})

		if request.method == 'POST':
			if 'code' in request.POST:

				# try:
				code = request.POST['code']	
				print(code)
				if code:
					clas = Classroom.objects.get(code = code)
					x = clas.students.all().exists()
					z = clas.students.all()
					
					if x:
						for i in z:
							print(username==i.username)
							if username.strip() != str(i.username).strip():
								c.classroom.add(clas)
								messages.warning(request, 'classroom added successfully')
								return HttpResponseRedirect('/%s/'%request.user.username)
							else:
								messages.warning(request, 'you are already in classroom')
								return HttpResponseRedirect('/%s/'%request.user.username)
					
							
					else:
						c.classroom.add(clas)	
						return HttpResponseRedirect('/%s/'%request.user.username)

				# except Exception as e:
				# 	messages.warning(request, 'classroom Doest not exists')
				
				
					
				# except:
					# messages.warning(request, 'Invalid code')
	try:
		slug = request.POST["query"]
		if slug:
			print(slug)
			query = slugify(slug)
			return HttpResponseRedirect('/search/%s/'%query)
	except Exception as e:
		pass
	
	return render(request, "student_dashboard.html", context)

@login_required
def classroom_full(request,username = None,  slug = None):
	if not request.user.is_authenticated:
		raise Http404
	clas = Classroom.objects.get(slug = slug)
	member = student.objects.filter(classroom = clas)
	print(member)
	posts = Post.objects.filter(classroom = clas).order_by("-timestamp")
	form = None
	context = {"form":form, "posts":posts,'class':clas}
	group_id = User.objects.filter(username = request.user.username).values('groups')
	group = str(Group.objects.get(id = group_id))
	paginator = Paginator(posts, 5)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)

	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)
	t = teacher.objects.get(username = clas.teacher)
	print(t.email) 
	context = {
		"object_list":queryset,
		"title": "list",
		"page_request_var":page_request_var,
		"form":form,
		"posts":posts,
		'class':clas,
		'member':member,
		'teacher':t,
	}
	if 'teacher' in group :
		form = PostForm(request.POST or None)
		fileForm = FileForm(request.POST or None, request.FILES or None) 

		context.update({'form':form, 'fileform':fileForm, 'author':True})
		if form.is_valid() and fileForm.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.classroom = clas
			slug = create_slug(instance)
			instance.slug = slug
			instance.save()
			if request.FILES :
				for f in request.FILES.getlist('file'):
					file.objects.create(Post = instance, file=f)
			return HttpResponseRedirect('/%s/%s/'%(request.user.username ,clas.slug))
			
			
	if 'student' in group :
		form =StudentPostForm(request.POST or None, request.FILES or None)
		fileForm = FileForm(request.POST or None, request.FILES or None) 

		context.update({'form':form, 'fileform':fileForm})
		if form.is_valid() and fileForm.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.classroom = clas
			slug = create_slug(instance)
			instance.slug = slug
			instance.post_type = 'post'
			instance.save()
			if request.FILES :
				for f in request.FILES.getlist('file'):
					file.objects.create(Post = instance, file=f)
			return HttpResponseRedirect('/%s/%s/'%(request.user.username ,clas.slug))

	try:
		slug = request.POST["query"]
		if slug:
			print(slug)
			query = slugify(slug)
			return HttpResponseRedirect('/search/%s/'%query)
	except Exception as e:
		pass

	return render(request, "classroom_detail.html", context)

@login_required
def post_full(request, username, slug):

	post = Post.objects.filter(slug = slug)
	instance = get_object_or_404(Post, slug = slug)
	files = file.objects.filter(Post = instance)
	group_id = User.objects.filter(username = request.user.username).values('groups')
	group = str(Group.objects.get(id = group_id))
	context = {'post': instance,'file':files}
	for p in post:
		if str(p.user).strip()==username.strip():
			context.update({'author': True})
		else:
			context.update({'author': False})
	print(context['author'],'/n',p.user,'/n',username.strip())
	try:
		slug = request.POST["query"]
		if slug:
			print(slug)
			query = slugify(slug)
			return HttpResponseRedirect('/search/%s/'%query)
	except Exception as e:
		pass

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	print(initial_data)
	form = CommentForm(request.POST or None, initial= initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		print('c_type : ',c_type)
		content_type = ContentType.objects.get(model=c_type)
		print(content_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)
		return HttpResponseRedirect("/%s/post/%s/"%(request.user.username, instance.slug))


	comments = instance.comments
	context.update({"comments":comments, "comment_form":form})
	return render(request, "post_detail.html", context)

@login_required
def post_edit(request, username, slug):
	instance = get_object_or_404(Post, user = request.user, slug = slug )
	files = file.objects.all().filter(Post=instance)
	group_id = User.objects.filter(username = request.user.username).values('groups')
	group = str(Group.objects.get(id = group_id))
	context = {'username':username, 'files':files, 'slug':slug}
	if 'teacher' in group :
		form = PostForm(request.POST or None, instance = instance)
		fileForm = FileForm(request.POST or None, request.FILES or None) 
		context.update({'form':form, 'fileform':fileForm})
		print(fileForm.is_valid())
		if form.is_valid() and fileForm.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			slug = create_slug(instance)
			instance.slug = slug
			instance.save()
			print(request.FILES)
			if request.FILES :
				for f in request.FILES.getlist('file'):
					print(f)
					file.objects.create(Post = instance, file=f)
				return HttpResponseRedirect('/%s/post/%s/'%(request.user.username,slug))
			
	if 'student' in group :
		form =StudentPostForm(request.POST or None, request.FILES or None, instance = instance)
		fileForm = FileForm(request.POST or None, request.FILES or None) 
		context.update({'form':form, 'fileform':fileForm})
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			slug = create_slug(instance)
			instance.slug = slug
			instance.post_type = 'post'
			instance.save()
			if request.FILES :
				for f in request.FILES.getlist('file'):
					file.objects.create(Post = instance, file=f)
				return HttpResponseRedirect('/%s/post/%s/'%(request.user.username,slug))
	return render(request, 'post_edit.html', context)


@login_required
def post_delete(request, username = None,  slug=None):
	instance = get_object_or_404(Post, slug = slug)
	classroom = instance.classroom
	slug = Classroom.objects.get(name = classroom)
	print(slug.slug)
	instance.delete()
	messages.success(request, '<h4 style = "margin :0 auto;">Post Deleted</h4>', extra_tags='html_safe')
	return HttpResponseRedirect("/%s/%s"%(request.user.username, slug.slug))

@login_required
def file_delete(request, username = None, file_name=None,  slug=None):
	instance = Post.objects.get(slug = slug)
	print(instance.id)
	instance2 = file.objects.get(Post=instance, file="Post/%s/%s"%(instance,file_name))
	print(instance2)
	instance2.delete()
	messages.success(request, '<h4 style = "margin :0 auto;">File Deleted</h4>', extra_tags='html_safe')
	return HttpResponseRedirect("/%s/post/%s/edit/"%(request.user.username, slug))



@login_required
def search(request, query):
	context = {}
	group_id = User.objects.filter(username = request.user.username).values('groups')
	group = str(Group.objects.get(id = group_id))
	try:
		stu = student.objects.filter(
			Q(first_name__icontains=query)|
			Q(last_name__icontains=query)|
			Q(middle_name__icontains=query)|
			Q(roll_no__icontains=query)|
			Q(batch__icontains=query)|
			Q(branch__icontains=query)|
			Q(email__icontains=query)|
			Q(contact__icontains=query)
			).distinct()
		context.update({'student':stu})
	except Exception as e:
		print(e)
		pass

	try:
		tea = teacher.objects.filter(
			Q(first_name__icontains=query)|
			Q(last_name__icontains=query)|
			Q(middle_name__icontains=query)|
			Q(address__icontains=query)|
			Q(email__icontains=query)|
			Q(contact__icontains=query)|
			Q(position__icontains=query)
			).distinct()
		context.update({'teacher':tea})
	except Exception as e:
		pass
	if 'teacher' in group :
		t1 = Classroom.objects.filter(teacher = request.user).values('id')
		l = []

		try:
			for j in t1:
				print(j)
				l.append(j['id'])
			print(l)
		except:
			pass
		try:
			post = Post.objects.filter(
				Q(title__icontains=query)|
				Q(slug__icontains=query)|
				Q(content__icontains=query)
				).filter(classroom__in = l).distinct()
			context.update({'post':post})

		except Exception as e:
			raise e

	
		try:
			print(Classroom.objects.filter(Q(teacher__exact=request.user)))
			clas = Classroom.objects.filter(
				Q(name__icontains=query)|
				Q(description__icontains=query)|
				Q(slug__icontains=query)
				).filter(pk__in = l).distinct()
			context.update({'classroom':clas})
		except Exception as e:
			raise e

	if 'student' in group:
		c1 = student.objects.filter(username = request.user).values('classroom')
		l=[]
		try:
			for j in c1:
				l.append(int(j['classroom']))
		except:
			pass	

		try:
			post = Post.objects.filter(
				Q(title__icontains=query)|
				Q(slug__icontains=query)|
				Q(content__icontains=query)
				).filter(classroom__in = l)
			context.update({'post':post})

		except:
			pass

		cl = Classroom.objects.filter(
			Q(name__icontains = query)|
			Q(description__icontains = query)
			 ).filter(pk__in = l)
		
		context.update({'classroom':cl})
	try:
		slug = request.POST["query"]
		if slug:
			print(slug)
			query = slugify(slug)
			return HttpResponseRedirect('/search/%s/'%query)
	except Exception as e:
		pass

	print(context)
	return render(request, 'search.html', context)


@login_required
def profile(request, username):
	context = {}
	if request.user.username==username:
		context.update({'author':True})
	group_id = User.objects.filter(username = username).values('groups')
	group = str(Group.objects.get(id = group_id))
	if 'teacher' in group:
		t1 = User.objects.get(username = username)
		t = teacher.objects.filter(username = t1)
		c = Classroom.objects.filter(teacher = t1).order_by("-created")
		p = Post.objects.filter(user = t1).order_by("-timestamp")
		created = Fourms.objects.filter(creator = t1) 
		subscribed = Fourms.objects.filter(subscriber = t1)
		print(subscribed)
		context.update({'profile':t,'classroom':c,'post':p, 'created':created, 'subscribed':subscribed})
		queryset = teacher.objects.values_list('position',flat=True).get(username=request.user)
		if str(queryset).strip()=='principal' or str(queryset).strip()=='dean':
			all_c=Classroom.objects.filter()
			all_p=Post.objects.filter()
			all_f=Fourms.objects.filter()
			print(all_f)
			context.update({"principal":True,"allclassroom":all_c,"allpost":all_p, "allforums":all_f})
	if 'student' in group:
		user = User.objects.get(username = username)
		s = student.objects.filter(username = user)
		c1 = student.objects.filter(username = user).values('classroom')
		created = Fourms.objects.filter(creator = user) 
		subscribed = Fourms.objects.filter(subscriber = user)
		print(created, subscribed)
		l=[]
		try:
			for j in c1:
				l.append(int(j['classroom']))
		except:
			pass 

		c = Classroom.objects.filter(pk__in = l)
		p = Post.objects.filter(user = get_object_or_404(User, username=username))

		context.update({'profile':s,'classroom':c, 'post':p, 'created':created, 'subscribed':subscribed})
	try:
		slug = request.POST["query"]
		if slug:
			print(slug)
			query = slugify(slug)
			return HttpResponseRedirect('/search/%s/'%query)
	except Exception as e:
		pass

	return render(request, 'profile.html', context)


@login_required
def edit_profile(request,username):
	context = {}
	group_id = User.objects.filter(username = request.user.username).values('groups')
	group = str(Group.objects.get(id = group_id))
	user = get_object_or_404(User, username = request.user.username)
	if 'teacher' in group:
		instance = get_object_or_404(teacher, username = request.user)
		form = TeacherProfileForm(request.POST or None, request.FILES or None, instance = instance)
		context.update({'form':form})
		if form.is_valid():
			instance = form.save(commit = False)
			instance.first = False
			user.first_name = instance.first_name
			user.last_name = instance.last_name
			user.email = instance.email
			user.save()
			instance.save()
			return HttpResponseRedirect("/%s/profile/"%(request.user.username))

	if 'student' in group:
		instance = get_object_or_404(student, username = request.user)
		form = StudentProfileForm(request.POST or None, request.FILES or None, instance = instance)
		context.update({'form':form})
		if form.is_valid():
			instance = form.save(commit = False)
			instance.first = False
			instance.save()
			return HttpResponseRedirect("/%s/profile/"%(request.user.username))
	try:
		slug = request.POST["query"]
		if slug:
			print(slug)
			query = slugify(slug)
			return HttpResponseRedirect('/search/%s/'%query)
	except Exception as e:
		pass

	return render(request, "edit_profile.html", context)

@login_required
def changepassword(request, username):
	u = User.objects.get(username=request.user.username)
	if request.POST:
		password=request.POST.get('password')
		password1=request.POST.get('password1')
		print(password1.strip(),password)
		if password1.strip() == password.strip():
			print('True')
			u.set_password(password.strip())
			u.save()
			return HttpResponseRedirect("/")
		else:
			messages.error(request,'password does not match')
	return render(request, "changepassword.html", {})



@login_required
def create_user(request):
	print(request.user.is_authenticated,request.user.is_superuser, request.user.is_staff)
	if not request.user.is_authenticated and not request.user.is_superuser or not request.user.is_staff:
		messages.error(request,' 401 - Unauthorized: Access denied')
		HttpResponseRedirect('/error/')

	if request.method == "POST" and request.FILES['student']:
		file = request.FILES['student']
		write(file)
		return HttpResponse("OK", status=200)
	return render(request,"create_user.html", {})