# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

# from django import forms
from .models import (
    Exam,
    Question,
    Answer,
    ExamUserRelations,
)

admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(ExamUserRelations)
