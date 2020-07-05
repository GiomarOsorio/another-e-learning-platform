from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse_lazy
from courses.models import Course, CourseUserRelations
from django.http.response import Http404
from django.contrib import messages
from courses.models import Course
from django.db.models import Q

# Create your views here.


class PageViewFunctions(object):
    def get_courses_relations(self):
        my_courses = {}
        course = CourseUserRelations.objects.filter(user=self.request.user)
        if len(course) == 0:
            return {"empty": True}

        paginator = Paginator(course, 3)
        page = self.request.GET.get("my_courses")

        try:
            my_courses["courses_relations"] = paginator.get_page(page)
        except PageNotAnInteger:
            my_courses["courses_relations"] = paginator.get_page(1)
        except EmptyPage:
            my_courses["courses_relations"] = paginator.get_page(paginator.num_pages)

        return my_courses["courses_relations"]

    def get_courses_search(self, filter, query):
        my_courses = {}
        courses = Course.objects.filter(filter)

        my_courses["len"] = len(courses)
        my_courses["search"] = query

        paginator = Paginator(courses, 6)
        page = self.request.GET.get("page")

        try:
            my_courses["courses_instances"] = paginator.get_page(page)
        except PageNotAnInteger:
            my_courses["courses_instances"] = paginator.get_page(1)
        except EmptyPage:
            my_courses["courses_instances"] = paginator.get_page(paginator.num_pages)

        return my_courses


class HomeView(PageViewFunctions, View):
    template_name = "pages/home.html"

    def get(self, request, *args, **kwargs):
        content = {"courses_instances": Course.objects.all().order_by("?")[:3]}
        if request.user.is_authenticated:
            content["courses_relations"] = self.get_courses_relations()
        return render(request, self.template_name, content)


class SearchView(PageViewFunctions, View):
    template_name = "courses/courseListView.html"

    def get(self, request, search_text=None, *args, **kwargs):
        query = request.GET.get("q", None)
        if query is not None and len(query) > 0:
            or_lookup = (
                Q(tags__icontains=query)
                | Q(name__icontains=query)
                | Q(description__icontains=query)
            )
            return render(
                request, self.template_name, self.get_courses_search(or_lookup, query),
            )
        messages.warning(request, "empty searches cannot be processed.")
        return redirect("courses:course-list")

    def post(self, request, *args, **kwargs):
        messages.warning(
            request, "this request cannot be processed, please contact the admin."
        )
        return redirect("courses:course-list")

