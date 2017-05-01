import random
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from background.models import Background
# Create your models here.
def download_location(instance, filename):
	return "%s/%s"%(instance.id, filename)


class Classroom(models.Model):
	name = models.CharField(max_length=120, unique = True)
	slug = models.SlugField(unique=True, blank = True)
	teacher =  models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	code = models.CharField(max_length = 5)
	description = models.TextField(max_length = 400)
	created = models.DateTimeField(auto_now=False, auto_now_add=True)
	background = models.ForeignKey(Background, default = 1)
	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name



def create_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
	    slug = new_slug
	qs = Classroom.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
	    new_slug = "%s-%s" %(slug, qs.first().id)
	    return create_slug(instance, new_slug=new_slug)
	return slug

def background():
	a=list(Background.objects.values_list('id', flat=True))
	b=random.sample(a, 1)
	print(b[0])
	return Background.objects.get(id = b[0])