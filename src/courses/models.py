from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from users.models import User
from django.db import models

# Create your models here.
class Course(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    name = models.CharField(
        ("course name"),
        max_length=200,
        unique=False,
        blank=False,
        help_text=("Required. 200 characters or fewer."),
    )
    description = models.TextField(
        ("course description"),
        max_length=1500,
        unique=False,
        blank=False,
        help_text=("Required. 1500 characters or fewer."),
    )
    banner = models.ImageField(
        ("banner image"),
        default="default_banner.png",
        upload_to="banner_pics/",
        help_text=("maxime zise of 2MB. JPG ó PNG."),
        blank=True,
    )
    tags = models.TextField(
        ("tags"),
        unique=False,
        blank=False,
        help_text=("Required. to improve course searches"),
    )
    what_learn = models.TextField(
        ("what will you learn"),
        unique=False,
        blank=False,
        help_text=("Required. describes what they learn with the course."),
    )
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Course: " + self.name

    def save(self, *args, **kwargs):
        modules_list_forms = kwargs.pop("modules_list_forms", None)
        if kwargs.pop("update", None):
            Module.objects.filter(course=self).delete()
        super(Course, self).save(*args, **kwargs)
        if modules_list_forms:
            for module_form in modules_list_forms:
                module_instance = module_form.save(commit=False)
                module_instance.course = self
                module_instance.save(
                    segment_list=module_form.segments_forms(),
                    family_instance={"course": self},
                )

    def get_owner(self):
        return self.user.get_full_name()

    def get_modules_instances(self):
        modules_instances = Module.objects.filter(course=self)
        numbers_of_modules = [index + 1 for index in range(modules_instances.count())]

        return zip(numbers_of_modules, modules_instances)

    def get_detail_url(self):
        return reverse("courses:course-detail", kwargs={"id": self.id})

    def get_edit_url(self):
        return reverse("courses:course-update", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("courses:course-delete", kwargs={"id": self.id})

    def get_enroll_url(self):
        return reverse("courses:course-enroll", kwargs={"id": self.id})

    def get_home_url(self):
        return reverse("courses:course-home", kwargs={"id": self.id})

    def get_what_learns(self):
        return self.what_learn.split("%20")

    def get_tags(self):
        return self.tags.split("%20")


class Module(models.Model):
    course = models.ForeignKey(Course, default=None, on_delete=models.CASCADE)
    name = models.CharField(
        ("Module name"),
        max_length=120,
        unique=False,
        blank=False,
        help_text=("Required. 120 characters or fewer."),
    )

    def __str__(self):
        return "Module: " + self.name

    def save(self, *args, **kwargs):
        segment_list_forms = kwargs.pop("segment_list", None)
        family_instance = kwargs.pop("family_instance", None)
        super(Module, self).save(*args, **kwargs)
        if segment_list_forms:
            for segment_form in segment_list_forms:
                segment_instance = segment_form.save(commit=False)
                segment_instance.course = family_instance["course"]
                segment_instance.module = self
                segment_instance.save(
                    contents_list=segment_form.contents_forms(),
                    family_instance={
                        "course": family_instance["course"],
                        "module": self,
                    },
                )

    def get_home_url(self):
        return reverse(
            "courses:course-home-week",
            kwargs={"id": self.course.id, "idModule": self.id},
        )

    def get_segments_instances(self):
        return Segment.objects.filter(module=self)

    def belongs_to_the_course(self):
        return self.course


class Segment(models.Model):
    course = models.ForeignKey(Course, default=None, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, default=None, on_delete=models.CASCADE)
    name = models.CharField(
        ("segment name"),
        max_length=120,
        unique=False,
        blank=False,
        help_text=("Required. 120 characters or fewer."),
    )

    def __str__(self):
        return "Segment: " + self.name

    def save(self, *args, **kwargs):
        contents_list_forms = kwargs.pop("contents_list", None)
        family_instance = kwargs.pop("family_instance", None)
        super(Segment, self).save(*args, **kwargs)
        if contents_list_forms:
            for contentForm in contents_list_forms:
                content_instance = contentForm.save(commit=False)
                content_instance.course = family_instance["course"]
                content_instance.module = family_instance["module"]
                content_instance.segment = self
                content_instance.save()

    def get_contents_instances(self):
        return Content.objects.filter(segment=self)

    def belongs_to_the_course(self):
        return self.course

    def belongs_to_the_module(self):
        return self.module


class Content(models.Model):
    CONTENT_TYPE = [
        ("1", "Text (Plain)"),
        ("2", "Text (HTML FORMAT)"),
        ("3", "External Video"),
        ("4", "External Document"),
        ("5", "Exam"),
    ]
    course = models.ForeignKey(Course, default=None, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, default=None, on_delete=models.CASCADE)
    segment = models.ForeignKey(Segment, default=None, on_delete=models.CASCADE)
    content_type = models.CharField(
        ("content type"),
        max_length=2,
        choices=CONTENT_TYPE,
        help_text=("select the type of content."),
        blank=False,
        null=False,
        error_messages={
            "blank": ("you must select the type of content."),
            "null": ("you must select the type of content."),
        },
    )
    name = models.CharField(
        ("content name"),
        max_length=120,
        unique=False,
        blank=False,
        help_text=("Required. 120 characters or fewer."),
    )
    content = models.TextField(("Content"), blank=False, null=False, default="1",)

    def getType(self):
        if int(self.content_type) <= 2:
            return "Lecture"
        elif int(self.content_type) == 3:
            return "Video"
        elif int(self.content_type) == 4:
            return "Document"
        elif int(self.content_type) == 5:
            return "Exam"
        else:
            return "NF"

    def get_home_url(self):
        return reverse(
            "courses:course-home-week-content",
            kwargs={
                "id": self.course.id,
                "idModule": self.module.id,
                "idContent": self.id,
            },
        )

    def belongs_to_the_course(self):
        return self.course

    def belongs_to_the_module(self):
        return self.module

    def BelongsToTheSegment(self):
        return self.segment


class CourseUserRelations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
