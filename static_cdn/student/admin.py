from django.contrib import admin

# Register your models here.
from .models import student

class studentAdmin(admin.ModelAdmin):
	list_display = ["first_name", "roll_no", "branch","batch"]
	list_display_links = ["first_name", "roll_no", "branch","batch"]
	list_filter = ["branch","batch", "first_name", "roll_no"]
	search_fields = ["first_name", "roll_no", "branch","batch"]
	class Meta:
		model = student
			
admin.site.register(student, studentAdmin)