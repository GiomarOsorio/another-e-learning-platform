# courses/urls.py
from django.urls import path
from .views import (
    CourseListView,
    CourseDetailView,
    CourseCreateView,
    CourseUpdateView,
    CourseDeleteView,
    CourseMyListView,
    CourseExamManageView,
    CourseEnrollView,
    CourseHomeView,
    ModuleHomeView,
    ContentHomeView,
)

app_name = "courses"

urlpatterns = [
    path("", CourseListView.as_view(), name="course-list"),
    path("my-courses/", CourseMyListView.as_view(), name="course-my-list"),
    path(
        "manage-courses-exams/",
        CourseExamManageView.as_view(),
        name="course-owner-list",
    ),
    path("detail-<int:id>/", CourseDetailView.as_view(), name="course-detail"),
    path("create/", CourseCreateView.as_view(), name="course-create"),
    path("update-<int:id>/", CourseUpdateView.as_view(), name="course-update"),
    path("delete-<int:id>/", CourseDeleteView.as_view(), name="course-delete"),
    path("enroll-<int:id>/", CourseEnrollView.as_view(), name="course-enroll"),
    path("<int:id>/Home/", CourseHomeView.as_view(), name="course-home"),
    path(
        "<int:id>/Home/<int:idModule>",
        ModuleHomeView.as_view(),
        name="course-home-week",
    ),
    path(
        "<int:id>/Home/<int:idModule>/<int:idContent>",
        ContentHomeView.as_view(),
        name="course-home-week-content",
    ),
]
