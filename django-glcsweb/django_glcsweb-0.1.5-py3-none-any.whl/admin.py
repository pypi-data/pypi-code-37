from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Instructor)
admin.site.register(ProjectSettings)
admin.site.register(Credentials)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Assignment)
