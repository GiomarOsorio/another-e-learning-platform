from django import forms
from PIL import Image
from exams.models import Exam
from .models import (
    Course,
    Module,
    Segment,
    Content,
)


class ContentCreate(forms.ModelForm):
    class Meta:
        model = Content
        fields = ["name", "content_type", "content"]

    def get_exam_name(self):
        idExam = self.cleaned_data.get("content", False)
        try:
            return Exam.objects.get(id=idExam).name
        except Exam.DoesNotExist:
            return ""


class SegmentCreate(forms.ModelForm):
    contents_list = []

    class Meta:
        model = Segment
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        contents = kwargs.pop("contents", None)
        super(SegmentCreate, self).__init__(*args, **kwargs)
        if contents:
            self.contents_list = []
            for iContent in contents:
                self.contents_list.append(ContentCreate(contents[iContent]))

    def is_valid(self):
        """Return True if the form has no errors, or False otherwise."""
        if self.is_bound and not self.errors:
            valid = True
        else:
            return False
        for contentForm in self.contents_list:
            if not contentForm.is_valid():
                valid = False
        return valid

    def contents_forms(self):
        return self.contents_list


class ModuleCreate(forms.ModelForm):
    segment_list = []

    class Meta:
        model = Module
        fields = [
            "name",
        ]

    def __init__(self, *args, **kwargs):
        segments = kwargs.pop("segments", None)
        super(ModuleCreate, self).__init__(*args, **kwargs)
        if segments:
            self.segment_list = []
            for iSegment in segments:
                contents_data = segments[iSegment].pop("Contents")
                self.segment_list.append(
                    SegmentCreate(segments[iSegment], contents=contents_data)
                )

    def is_valid(self):
        """Return True if the form has no errors, or False otherwise."""
        if self.is_bound and not self.errors:
            valid = True
        else:
            return False
        for segment_form in self.segment_list:
            if not segment_form.is_valid():
                valid = False
        return valid

    def segments_forms(self):
        return self.segment_list


class CourseCreate(forms.ModelForm):
    module_Template = ModuleCreate()
    segment_template = SegmentCreate()
    content_template = ContentCreate()
    module_list = []

    class Meta:
        model = Course
        fields = ["name", "description", "banner", "tags", "what_learn"]

    def __init__(self, *args, **kwargs):
        modules = kwargs.pop("modules", None)
        super(CourseCreate, self).__init__(*args, **kwargs)
        if modules:
            self.module_list = []
            for i_module in modules:
                segments_data = modules[i_module].pop("Segments")
                self.module_list.append(
                    ModuleCreate(modules[i_module], segments=segments_data)
                )

    def is_valid(self):
        """Return True if the form has no errors, or False otherwise."""
        if self.is_bound and not self.errors:
            valid = True
        else:
            return False
        for module_form in self.module_list:
            if not module_form.is_valid():
                valid = False
        return valid

    def clean_banner(self):
        banner = self.cleaned_data.get("banner", False)

        if type(banner).__name__ == "ImageFieldFile":
            return banner
        elif banner and type(banner).__name__ == "InMemoryUploadedFile":
            if len(banner) > 2 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 2MB )")
            _, sub = banner.content_type.split("/")
            if not sub in ["jpeg", "pjpeg", "png"]:
                raise forms.ValidationError(u"Please use a JPEG, or PNG image.")
            return banner
        else:
            raise forms.ValidationError("Couldn't read uploaded image")

    def has_children_forms(self):
        return False if len(self.module_list) == 0 else True

    def modules_forms(self):
        return self.module_list

    def get_module_template(self):
        return self.module_Template

    def get_segment_template(self):
        return self.segment_template

    def get_content_template(self):
        return self.content_template
