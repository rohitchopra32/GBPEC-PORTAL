from django.contrib import admin

# Register your models here.
from .models import teacher

class teacherAdmin(admin.ModelAdmin):

	list_display = ["first_name", "email", "contact"]
	list_display_links = ["first_name", "email", "contact"]
	list_filter = ["first_name", "email", "contact"]
	search_fields = ["first_name", "email", "contact"]
	class Meta:
		model = teacher
			
admin.site.register(teacher, teacherAdmin)