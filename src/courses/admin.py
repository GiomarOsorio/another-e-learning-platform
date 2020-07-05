from django.contrib import admin

# Register your models here.
from .models import (
    Course,
    Module,
    Segment,
    Content,
    CourseUserRelations,
)

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Segment)
admin.site.register(Content)
admin.site.register(CourseUserRelations)
