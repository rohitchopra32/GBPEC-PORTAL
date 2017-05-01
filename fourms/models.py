import random
from django.db import models
from django.conf import settings
from django.utils.text import slugify


# Create your models here.
def forum_upload_location(instance, filename):
    return "Forums/%s/%s" %(instance.title, filename)


def post_upload_location(instance, filename):
	return "forum_post/%s/%s"%(instance.slug,filename)


class category(models.Model):
	name = models.CharField(max_length=120, unique=True)
	description = models.CharField(max_length = 500, blank=True)
	created = models.DateTimeField(auto_now_add = True, auto_now = False)
	updated = models.DateTimeField(auto_now_add = False, auto_now = True)
	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name




class Fourms(models.Model):
	title = models.CharField(max_length=120, null=True)
	category = models.ForeignKey(category, null=True, on_delete=models.CASCADE)
	slug = models.SlugField(unique=True, blank = True)
	creator =  models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	description = models.TextField(max_length = 400)
	file = models.FileField(upload_to=forum_upload_location, null=True, blank=True)
	created = models.DateTimeField(auto_now=False, auto_now_add=True)
	subscriber = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subscriber', blank=True)
	
	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def filename(self):
		f = self.file.name
		f1 = f.split('/', 3)[-1]
		return f1


	def postcount(instance):
		count = forumPost.objects.filter(forum=instance).count()
		return count

def create_forum_slug(instance, new_slug=None):
		slug = slugify(instance.title)
		if new_slug is not None:
		    slug = new_slug
		qs = Fourms.objects.filter(slug=slug).order_by("-id")
		exists = qs.exists()
		if exists:
		    new_slug = "%s-%s" %(slug, qs.first().id)
		    return create_forum_slug(instance, new_slug=new_slug)
		return slug



class forumPost(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	slug = models.SlugField(unique=True, blank = True)
	content = models.TextField()
	file = models.FileField(upload_to=post_upload_location, null = True, blank = True)
	forum = models.ForeignKey(Fourms, on_delete=models.CASCADE)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	

	def __unicode__(self):
	    return self.slug

	def __str__(self):
	    return self.slug

	def filename(self):
		f = self.file.name
		f1 = f.split('/', 3)[-1]
		return f1

	@property
	def comments(self):
	    instance = self
	    qs = Comment.objects.filter_by_instance(instance)
	    return qs

	@property
	def get_content_type(self):
	    instance = self
	    content_type = ContentType.objects.get_for_model(instance.__class__)
	    return content_type.model

	def get_absolute_url(self):
	    return reverse("posts:detail", kwargs={"slug": self.slug})

	


def create_post_slug(instance, new_slug=None):
		slug = slugify(instance.id)
		if new_slug is not None:
		    slug = new_slug
		qs = forumPost.objects.filter(slug=slug).order_by("-id")
		exists = qs.exists()
		if exists:
		    new_slug = "%s-%s" %(slug, qs.first().id)
		    return create_post_slug(instance, new_slug=new_slug)
		return slug


