from django.contrib import admin

# Register your models here.
from .models import student

class studentAdmin(admin.ModelAdmin):
	list_display = ["name", "roll_no", "branch","batch","password"]
	list_display_links = ["name", "roll_no", "branch","batch"]
	list_filter = ["branch","batch", "name", "roll_no"]
	search_fields = ["name", "roll_no", "branch","batch"]
	class Meta:
		model = student
			
admin.site.register(student, studentAdmin)