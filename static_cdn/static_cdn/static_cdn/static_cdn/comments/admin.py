from django.contrib import admin

# Register your models here.
from .models import Comment

class CommentModelAdmin(admin.ModelAdmin):
	list_display = ["user", "content_type", "object_id", "parent", "content"]
	list_display_links = ["user", "content_type", "object_id", "parent", "content"]
	list_filter = ["user", "content_type", "object_id", "parent", "content"]
	search_fields = ["user", "content_type", "object_id", "parent", "content"]
	class Meta:
		model = Comment


admin.site.register(Comment, CommentModelAdmin)