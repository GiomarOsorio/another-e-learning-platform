from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http.response import HttpResponse
from django.contrib import messages
from .forms import CourseCreate
from django.urls import reverse
from django.http import Http404
from django.views import View
from .models import Course, Module, Content, CourseUserRelations
from exams.models import Exam, ExamUserRelations
import json, re

import base64
import io
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile
from mimetypes import guess_extension


class CoursesViewFunctions(object):
    courses = {}
    course_data = {}

    def get_courses(self):
        course = Course.objects.all()
        len(course)
        if len(course) == 0:
            return {"empty": True}

        paginator = Paginator(course, 6)
        page = self.request.GET.get("page")

        try:
            self.courses["courses_instances"] = paginator.get_page(page)
        except PageNotAnInteger:
            self.courses["courses_instances"] = paginator.get_page(1)
        except EmptyPage:
            self.courses["courses_instances"] = paginator.get_page(paginator.num_pages)

        return self.courses

    def get_owner_courses_exams(self):
        user = {"CoursesEmpty": False, "ExamsEmpty": False}
        if self.request.user.is_admin:
            course = Course.objects.all()
            exam = Exam.objects.all()
        else:
            course = Course.objects.filter(user=self.request.user)
            exam = Exam.objects.filter(user=self.request.user)

        if len(course) == 0:
            user["CoursesEmpty"] = True
        else:
            course_paginator = Paginator(course, 3)
            course_page = self.request.GET.get("coursepage")

            try:
                user["Courses"] = course_paginator.get_page(course_page)
            except PageNotAnInteger:
                user["Courses"] = course_paginator.get_page(1)
            except EmptyPage:
                user["Courses"] = course_paginator.get_page(course_paginator.num_pages)

        if len(exam) == 0:
            user["ExamsEmpty"] = True
        else:
            exam_paginator = Paginator(exam, 3)
            exam_page = self.request.GET.get("exampage")

            try:
                user["Exams"] = exam_paginator.get_page(exam_page)
            except PageNotAnInteger:
                user["Exams"] = exam_paginator.get_page(1)
            except EmptyPage:
                user["Exams"] = exam_paginator.get_page(exam_paginator.num_pages)

        return user

    def get_course_instance(self):
        id = self.kwargs.get("id")
        course = None
        if id is not None:
            course = get_object_or_404(Course, id=id)
        return course

    def get_module_instance(self):
        id = self.kwargs.get("idModule")
        module = None
        if id is not None:
            module = get_object_or_404(Module, id=id)
        return module

    def get_content_instance(self):
        id = self.kwargs.get("idContent")
        content = None
        relation = None
        if id is not None:
            content = get_object_or_404(Content, id=id)
            if type(content).__name__ == "Content":
                if content.content_type == "5":
                    try:
                        relation = ExamUserRelations.objects.get(
                            user=self.request.user, exam=content.exam
                        )
                    except ExamUserRelations.DoesNotExist:
                        relation = None
                    return {"content": content, "relation": relation}
        return content

    def get_course_user_relation(self):
        user = {"courses_empty": False}
        course = CourseUserRelations.objects.filter(user=self.request.user)

        if len(course) == 0:
            user["courses_empty"] = True
        else:
            course_paginator = Paginator(course, 3)
            course_page = self.request.GET.get("coursepage")

            try:
                user["courses_relations"] = course_paginator.get_page(course_page)
            except PageNotAnInteger:
                user["courses_relations"] = course_paginator.get_page(1)
            except EmptyPage:
                user["courses_relations"] = course_paginator.get_page(
                    course_paginator.num_pages
                )

        return user

    def relation_exist(self):
        id = self.kwargs.get("id")
        if id is None:
            return None

        try:
            course_instance = Course.objects.get(id=id)
        except Course.DoesNotExist:
            return None

        try:
            relation = CourseUserRelations.objects.get(
                user=self.request.user, course=course_instance
            )
            return True
        except CourseUserRelations.DoesNotExist:
            return False

    def to_file(self, image, picture_name):
        """base64 encoded file to Django InMemoryUploadedFile that can be placed into request.FILES."""
        # 'data:image/png;base64,<base64 encoded string>'
        try:
            idx = image[:50].find(",")

            if not idx or not image.startswith("data:image/"):
                raise Exception()

            base64file = image[idx + 1 :]
            attributes = image[:idx]
            content_type = attributes[len("data:") : attributes.find(";")]
        except Exception as e:
            return None

        f = io.BytesIO(base64.b64decode(base64file))
        image = InMemoryUploadedFile(
            f,
            field_name="banner",
            name=picture_name + guess_extension(content_type),
            content_type=content_type,
            size=sys.getsizeof(f),
            charset=None,
        )
        return image


class CourseCreateView(CoursesViewFunctions, View):
    template_name = "courses/courseCreateView.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("pages:login-page")
        if not request.user.has_permissions:
            messages.error(
                request, "You do not have sufficient permissions to use this feature"
            )
            return redirect("pages:home-page")
        return render(
            request,
            self.template_name,
            {
                "course_form": CourseCreate(),
                "exams_instances": Exam.objects.filter(content=None, user=request.user),
            },
        )

    def post(self, request, *args, **kwargs):
        if not request.user.has_permissions:
            messages.error(
                request, "You do not have sufficient permissions to use this feature"
            )
            return redirect("pages:home-page")
        if request.is_ajax:
            course_data = json.loads(self.request.body)["Course"]
            banner = self.to_file(
                course_data.pop("banner"), course_data["name"] + "_banner"
            )
            course_modules_data = course_data.pop("Modules")
            if banner is not None:
                request.FILES["banner"] = banner
            course = CourseCreate(
                course_data, request.FILES, modules=course_modules_data
            )
            if course.is_valid():
                course_instance = course.save(commit=False)
                course_instance.user = self.request.user
                course_instance.save(modules_list_forms=course.modules_forms())
                messages.success(request, "Course created successfully")
                return HttpResponse(
                    json.dumps(
                        {
                            "error": False,
                            "url_redirect": reverse("courses:course-owner-list"),
                        }
                    )
                )
            messages.error(request, "There is an error in the form.")
            html = (
                render_to_string(
                    self.template_name,
                    {
                        "course_form": course,
                        "exams_instances": Exam.objects.filter(
                            content=None, user=request.user
                        ),
                    },
                    request,
                )
                + ""
            )
            body = re.findall("<body>(.*?)</body>", html, re.DOTALL)
            return HttpResponse(json.dumps({"error": True, "content": body}))
        messages.error(request, "An error has occurred, please try again later.")
        return redirect("pages:home-page")


class CourseListView(CoursesViewFunctions, View):
    template_name = "courses/courseListView.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("pages:login-page")
        return render(request, self.template_name, self.get_courses())


class CourseMyListView(CoursesViewFunctions, View):
    template_name = "courses/courseMyListView.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("pages:login-page")
        return render(request, self.template_name, self.get_course_user_relation())


class CourseExamManageView(CoursesViewFunctions, View):
    template_name = "courses/courseExamManageView.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("pages:login-page")
        if not request.user.has_permissions:
            messages.error(
                request, "You do not have sufficient permissions to use this feature"
            )
            return redirect("pages:home-page")
        return render(request, self.template_name, self.get_owner_courses_exams())


class CourseDetailView(CoursesViewFunctions, View):
    template_name = "courses/courseDetailView.html"

    def get(self, request, id=None, *args, **kwargs):
        course = self.get_course_instance()
        if course is not None:
            owner = False
            registered = False
            if request.user.is_authenticated:
                owner = True if self.request.user == course.user else False
                registered = True if self.relation_exist() else False
            return render(
                request,
                self.template_name,
                {"course_instance": course, "Owner": owner, "Registered": registered},
            )
        messages.error(request, "that course doesn't exist")
        return redirect("courses:course-list")


class CourseDeleteView(CoursesViewFunctions, View):
    def get(self, request, id=None, *args, **kwargs):
        return redirect("pages:home-page")

    def post(self, request, *args, **kwargs):
        if not request.user.has_permissions:
            messages.error(
                request, "You do not have sufficient permissions to use this feature"
            )
            return redirect("pages:home-page")
        course = self.get_course_instance()
        if course is not None:
            if (course.user == request.user) or request.user.is_admin:
                course.delete()
                messages.success(request, "Course delete")
                return redirect("courses:course-owner-list")
            return redirect("courses:course-list")
        messages.error(request, "That course doesn't exist")
        return redirect("courses:course-owner-list")


class CourseUpdateView(CoursesViewFunctions, View):
    template_name = "courses/courseUpdateView.html"

    def get(self, request, id=None, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("pages:login-page")
        if not request.user.has_permissions:
            messages.error(
                request, "You do not have sufficient permissions to use this feature"
            )
            return redirect("pages:home-page")
        course = self.get_course_instance()
        if course is not None:
            return render(
                request,
                self.template_name,
                {
                    "course_instance": course,
                    "course_form": CourseCreate(),
                    "exams_instances": Exam.objects.filter(
                        content=None, user=course.user
                    ),
                },
            )
        messages.error(request, "That course doesn't exist")
        return redirect("courses:course-list")

    def post(self, request, *args, **kwargs):
        if not request.user.has_permissions:
            messages.error(
                request, "You do not have sufficient permissions to use this feature"
            )
            return redirect("pages:home-page")
        if request.is_ajax:
            courseObject = self.get_course_instance()
            if courseObject is not None:
                course_data = json.loads(self.request.body)["Course"]
                banner = self.to_file(
                    course_data.pop("banner"), course_data["name"] + "_banner"
                )
                course_modules_data = course_data.pop("Modules")
                if banner is not None:
                    request.FILES["banner"] = banner
                course = CourseCreate(
                    course_data,
                    request.FILES,
                    modules=course_modules_data,
                    instance=self.get_course_instance(),
                )
                if course.is_valid():
                    course_instance = course.save(commit=False)
                    course_instance.save(
                        module_list=course.modules_forms(), update=True
                    )
                    messages.success(
                        request, "The course has been successfully edited."
                    )
                    return HttpResponse(
                        json.dumps(
                            {
                                "error": False,
                                "url_redirect": reverse("courses:course-owner-list"),
                            }
                        )
                    )
                messages.error(request, "There is an error in the form.")
                html = (
                    render_to_string(
                        self.template_name,
                        {
                            "course_instance": courseObject,
                            "course_form": course,
                            "exams_instances": Exam.objects.filter(
                                content=None, user=self.get_course_instance().user
                            ),
                        },
                        request,
                    )
                    + ""
                )
                body = re.findall("<body>(.*?)</body>", html, re.DOTALL)
                return HttpResponse(json.dumps({"error": True, "content": body}))
            messages.error(request, "that course doesn't exist")
            return redirect("courses:course-list")
        messages.error(request, "An error has occurred, please try again later")
        return redirect("pages:home-page")


class CourseEnrollView(CoursesViewFunctions, View):
    def get(self, request, id=None, *args, **kwargs):
        return redirect("pages:home-page")

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "you need to login to register for a course")
            return redirect("pages:login-page")
        relation = self.relation_exist()
        course = self.get_course_instance()
        if relation:
            messages.success(request, "You are already enrolled in this course.")
            return redirect(course.get_detail_url())
        elif not relation:
            CourseUserRelations.objects.create(user=self.request.user, course=course)
            messages.success(request, "You have successfully enrolled in the course.")
            return redirect(course.get_detail_url())
        messages.error(request, "An error has occurred, please try again later.")
        return redirect("courses:course-list")


class CourseHomeView(CoursesViewFunctions, View):
    template_name = "courses/courseHomeView.html"

    def get(self, request, id, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "you need to login to register for a course.")
            return redirect("pages:login-page")
        registered = True if self.relation_exist() else False
        course = self.get_course_instance()
        if not self.relation_exist():
            messages.success(
                request, "You need to register to view the course content.",
            )
            return redirect(course.get_detail_url())
        module = Module.objects.filter(course=course)[0]
        return render(
            request,
            self.template_name,
            {"course_instance": course, "module_instance": module,},
        )


class ModuleHomeView(CoursesViewFunctions, View):
    template_name = "courses/courseHomeView.html"

    def get(self, request, id, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "you need to login to register for a course.")
            return redirect("pages:login-page")
        registered = True if self.relation_exist() else False
        course = self.get_course_instance()
        if not self.relation_exist():
            messages.success(
                request, "You need to register to view the course content.",
            )
            return redirect(course.get_detail_url())
        module = self.get_module_instance()
        return render(
            request,
            self.template_name,
            {"course_instance": course, "module_instance": module,},
        )


class ContentHomeView(CoursesViewFunctions, View):
    template_name = "courses/courseContentView.html"

    def get(self, request, id, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "you need to login to register for a course.")
            return redirect("pages:login-page")
        registered = True if self.relation_exist() else False
        course = self.get_course_instance()
        if not self.relation_exist():
            messages.success(
                request, "You need to register to view the course content.",
            )
            return redirect(course.get_detail_url())
        module = self.get_module_instance()
        content = self.get_content_instance()
        if type(content).__name__ != "dict":
            return render(
                request,
                self.template_name,
                {
                    "course_instance": course,
                    "module_instance": module,
                    "content_instance": content,
                },
            )
        return render(
            request,
            self.template_name,
            {
                "course_instance": course,
                "module_instance": module,
                "content_instance": content["content"],
                "relation": content["relation"],
            },
        )

