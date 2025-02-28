from django.contrib import admin
from .models import College, CustomUser,Teacher,Section,Student,Subject,Course,Department

admin.site.register(College)
admin.site.register(CustomUser)
admin.site.register(Section)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Department)
