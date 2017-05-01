from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)

class post(models.Model):
	title = models.CharField(max_length=120)
	content = models.TextField()
	attachment =models.FileField(upload_to=upload_location,null=True, blank=True)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	email = models.EmailField(max_length = 100, null= True)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
	object_id = models.PositiveIntegerField(null=True)
	content_object = GenericForeignKey('content_type', 'object_id')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse(":post:detail", kwargs={"username":self.content_type,"id": self.id})

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type