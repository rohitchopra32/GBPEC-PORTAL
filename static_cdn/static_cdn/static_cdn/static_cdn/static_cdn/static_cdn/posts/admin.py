from django.contrib import admin

# Register your models here.
from .models import classPost, file

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["user", "title", "updated", "timestamp"]
	list_display_links = ["user", "title","updated"]
	list_filter = ["title", "content", "user", "classroom", "updated", "timestamp"]
	search_fields = ["title", "content", "user", "classroom"]
	class Meta:
		model = classPost




class fileAdmin(admin.ModelAdmin):
	list_display = ["Post", "file"]
	list_display_links = ["Post", "file"]
	list_filter = ["Post", "file", "timestamp"]
	search_fields = ["Post", "file", "timestamp"]
	class Meta:
		model = file


admin.site.register(file, fileAdmin)
admin.site.register(classPost, PostModelAdmin)
