from django.urls import path
from .views import (
    ExamDetailView,
    ExamCreateView,
    ExamUpdateView,
    ExamDeleteView,
    ExamTakeView,
    examEvaluatedView,
)

app_name = "exams"

urlpatterns = [
    path("detail-<int:id>/", ExamDetailView.as_view(), name="exam-detail"),
    path("create/", ExamCreateView.as_view(), name="exam-create"),
    path("update-<int:id>/", ExamUpdateView.as_view(), name="exam-update"),
    path("delete-<int:id>/", ExamDeleteView.as_view(), name="exam-delete"),
    path("<int:idExam>/", ExamTakeView.as_view(), name="exam-take"),
    path("<int:idExam>/evaluated/", examEvaluatedView.as_view(), name="exam-evaluated")
]
