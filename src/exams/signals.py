from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import (
    Content,
    CourseUserRelations,
)

from .models import Exam
from .models import ExamUserRelations


@receiver(post_save, sender=Content)
def content_exam_relations(sender, instance, **kwargs):
    if instance.content_type == "5" and instance.content != None:
        try:
            exam_instance = Exam.objects.get(id=instance.content)
            exam_instance.content = instance
            exam_instance.save()
        except ObjectDoesNotExist:
            print("This exam cannot be related.")


@receiver(post_save, sender=CourseUserRelations)
def exams_user_relations(sender, instance, created, **kwargs):
    if created:
        content_with_exam = Content.objects.filter(
            course=instance.course, content_type="5"
        )
        if len(content_with_exam) > 0:
            for content in content_with_exam:
                try:
                    exam_instance = Exam.objects.get(id=content.content)
                    ExamUserRelations.objects.create(
                        user=instance.user, exam=exam_instance,
                    )
                except ObjectDoesNotExist:
                    raise ("exam not exist in this course")
