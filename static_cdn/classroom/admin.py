from django.contrib import admin
from .models import Classroom 
# Register your models here.

class classroomAdmin(admin.ModelAdmin):
	list_display = ['name', 'teacher', 'created',]
	print(list_display)
	list_display_links = ["name", "teacher", "created" ]
	list_filter = ["name", "teacher", "created"]
	search_fields = ["name", "teacher", "created", "code", "description" ]
	class Meta:
		model = Classroom
			
admin.site.register(Classroom, classroomAdmin)