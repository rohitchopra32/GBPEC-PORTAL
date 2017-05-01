from django.contrib import admin
from .models import Background
# Register your models here.



class backgroundAdmin(admin.ModelAdmin):
	list_display = ['image']
	list_display_links = ["image"]
	list_filter = ["image"]
	search_fields = ["image" ]

	def admin_thumbnail(self):
		return u'<img src="%s" />' % (self.image.url)
	
	admin_thumbnail.short_description = 'Thumbnail'
	admin_thumbnail.allow_tags = True
	
	class Meta:
		model = Background
			


admin.site.register(Background, backgroundAdmin)