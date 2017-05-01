from django.contrib import admin

# Register your models here.
from .models import post

class postadmin(admin.ModelAdmin):
	list_display = ["title", "updated", "timestamp"]
	list_display_links = ["updated", "title"]
	list_filter = ["updated", "timestamp"]
	search_fields = ["title", "content"]
	class Meta:
		model = post
			
admin.site.register(post, postadmin)

