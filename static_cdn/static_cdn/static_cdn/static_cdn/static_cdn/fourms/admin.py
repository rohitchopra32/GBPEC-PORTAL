from django.contrib import admin
from .models import Fourms, category, forumPost

# Register your models here.

class ForumsAdmin(admin.ModelAdmin):
	list_display = ["creator", "title", "created", "category"]
	list_display_links = ["creator", "title","created"]
	list_filter = ["title", "creator", "category", "created", "subscriber"]
	search_fields = ["title", "content", "creator", "category", "subscriber"]
	class Meta:
		model = Fourms




class forumpostAdmin(admin.ModelAdmin):
	list_display = ["forum", "user", "timestamp"]
	list_display_links = ["forum", "user", "timestamp"]
	list_filter = ["forum", "user", "timestamp", "updated","content"]
	search_fields = ["forum", "user", "timestamp", "updated","content"]
	class Meta:
		model = forumPost

class categoryAdmin(admin.ModelAdmin):
	list_display = ["name", "description"]
	list_display_links = ["name", "description"]
	list_filter = ["name", "description", "created", "updated"]
	search_fields = ["name", "description", "created", "updated"]
	class Meta:
		model = category



admin.site.register(category, categoryAdmin)
admin.site.register(forumPost, forumpostAdmin)
admin.site.register(Fourms, ForumsAdmin)