from django.db import models

# Create your models here.
def download_location(instance, filename):
	return "%s/%s"%(instance.id, filename)

class Background(models.Model):
	image = models.FileField(upload_to = download_location, null = True, blank = True)

	def __str__(self):
		return str(self.image)

	def __unicode__(self):
		return self.image