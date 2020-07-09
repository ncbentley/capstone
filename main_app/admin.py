from django.contrib import admin
from .models import Profile, Project, Page, Wireframe, Sprint, Task

# Register your models here.

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Page)
admin.site.register(Wireframe)
admin.site.register(Sprint)
admin.site.register(Task)