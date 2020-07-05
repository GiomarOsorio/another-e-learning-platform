from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http.response import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.http import Http404
from django.views import View
from .forms import ExamCreate
from .models import Exam, ExamUserRelations
import json, re


class ExamsViewFunctions(object):
    exams = {}
    exam_data = {}

    # def get_exams(self):
    #     exam = Exam.objects.filter(
    #         user = self.request.user
    #     )
    #     if len(exam)==0:
    #         return {'empty': True}

    #     paginator = Paginator(exam, 6)
    #     page = self.request.GET.get('page')

    #     try:
    #         self.exams['Exams'] = paginator.get_page(page)
    #     except PageNotAnInteger:
    #         self.exams['Exams'] = paginator.get_page(1)
    #     except EmptyPage:
    #         self.exams['Exams'] = paginator.get_page(paginator.num_pages)

    #     return self.exams

    def get_exam_instance(self):
        id = self.kwargs.get("id")
        exam = None
        if id is not None:
            exam = get_object_or_404(Exam, id=id)
        else:
            id = self.kwargs.get("idExam")
            if id is not None:
                exam = get_object_or_404(Exam, id=id)
        return exam


class ExamCreateView(View):
    template_name = "exams/examCreateView.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("pages:login-page")
        if not request.user.has_permissions:
            messages.error(
                request, "You do not have sufficient permissions to use this feature"
            )
            return redirect("pages:home-page")
        return render(request, self.template_name, {"exam_form": ExamCreate()})

    def post(self, request, *args, **kwargs):
        if not request.user.has_permissions:
            messages.error(
                request, "You do not have sufficient permissions to use this feature"
            )
            return redirect("pages:home-page")
        if request.is_ajax():
            exam_data = json.loads(self.request.body)["Exam"]
            exam_questions_data = exam_data.pop("Questions")
            exam = ExamCreate(exam_data, questions=exam_questions_data)
            if exam.is_valid():
                exam_instance = exam.save(commit=False)
                exam_instance.user = self.request.user
                exam_instance.save(questionlist=exam.questions_forms())
                messages.success(request, "Se creado el exam satisfatoriamente")
                return HttpResponse(
                    json.dumps(
                        {
                            "error": False,
                            "url_redirect": reverse("courses:course-owner-list"),
                        }
                    )
                )
            messages.error(request, "Existe un error en el formulario.")
            html = (
                render_to_string(self.template_name, {"exam_form": exam}, request) + ""
            )
            body = re.findall("<body>(.*?)</body>", html, re.DOTALL)
            return HttpResponse(json.dumps({"error": True, "content": body}))
        messages.error(request, "Ha ocurrido un error, intente más tarde")
        return redirect("pages:home-page")


class ExamDetailView(ExamsViewFunctions, View):
    template_name = "exams/examDetailView.html"

    def get(self, request, id=None, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("pages:login-page")
        if not request.user.has_permissions:
            messages.error(
                request, "You do not have sufficient permissions to use this feature"
            )
            return redirect("pages:home-page")
        exam = self.get_exam_instance()
        if exam is not None:
            return render(request, self.template_name, {"exam_instance": exam})
        messages.error(request, "that exam doesn't exist")
        return redirect("exams:exam-list")


class ExamDeleteView(ExamsViewFunctions, View):
    def get(self, request, id=None, *args, **kwargs):
        return redirect("pages:home-page")

    def post(self, request, *args, **kwargs):
        if not request.user.has_permissions:
            messages.error(
                request, "You do not have sufficient permissions to use this feature"
            )
            return redirect("pages:home-page")
        exam = self.get_exam_instance()
        if exam is not None:
            exam.delete()
            messages.success(request, "Exam delete")
            return redirect(reverse("courses:course-owner-list"))
        messages.error(request, "That exam doesn't exist")
        return redirect(reverse("courses:course-owner-list"))


class ExamUpdateView(ExamsViewFunctions, View):
    template_name = "exams/examUpdateView.html"

    def get(self, request, id=None, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("pages:login-page")
        if not request.user.has_permissions:
            messages.error(
                request, "You do not have sufficient permissions to use this feature"
            )
            return redirect("pages:home-page")
        exam = self.get_exam_instance()
        if exam is not None:
            return render(
                request,
                self.template_name,
                {"exam_instance": exam, "exam_form": ExamCreate()},
            )
        messages.error(request, "That exam doesn't exist")
        return redirect(reverse("exams:exam-list"))

    def post(self, request, *args, **kwargs):
        if not request.user.has_permissions:
            messages.error(
                request, "You do not have sufficient permissions to use this feature"
            )
            return redirect("pages:home-page")
        if request.is_ajax():
            exam_object = self.get_exam_instance()
            if exam_object is not None:
                exam_data = json.loads(self.request.body)["Exam"]
                exam_questions_data = exam_data.pop("Questions")
                exam = ExamCreate(
                    exam_data, questions=exam_questions_data, instance=exam_object
                )
                if exam.is_valid():
                    exam_instance = exam.save(commit=False)
                    exam_instance.user = self.request.user
                    exam_instance.save(questionlist=exam.questions_forms(), update=True)
                    messages.success(request, "Se editado el exam satisfatoriamente")
                    return HttpResponse(
                        json.dumps(
                            {
                                "error": False,
                                "url_redirect": reverse("courses:course-owner-list"),
                            }
                        )
                    )
                messages.error(request, "Existe un error en el formulario.")
                html = (
                    render_to_string(
                        self.template_name,
                        {"exam_instance": exam_object, "exam_form": exam},
                        request,
                    )
                    + ""
                )
                body = re.findall("<body>(.*?)</body>", html, re.DOTALL)
                return HttpResponse(json.dumps({"error": True, "content": body}))
            messages.error(request, "That exam doesn't exist")
            return redirect(reverse("courses:course-owner-list"))
        messages.error(request, "Ha ocurrido un error, intente más tarde")
        return redirect("pages:home-page")


class ExamTakeView(ExamsViewFunctions, View):
    template_name = "exams/ExamTakeView.html"

    def get(self, request, *args, **kwargs):
        return redirect("pages:home-page")

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("pages:login-page")
        exam = self.get_exam_instance()
        if exam is not None:

            try:
                relation = ExamUserRelations.objects.get(
                    user=self.request.user, exam=exam
                )
                if not relation.can_take_exam():
                    return redirect(exam.content.get_home_url())
            except ExamUserRelations.DoesNotExist:
                messages.error(
                    request,
                    "there is no relationship between the user and the exam, please contact the administrator.",
                )
                return redirect(exam.content.get_home_url())

            if not request.is_ajax():
                return render(request, self.template_name, {"exam_instance": exam})

            if request.is_ajax() and relation is not None:
                questions = json.loads(self.request.body)["Questions"]
                user_questions_evaluated = exam.evaluate(questions)
                relation.try_exam(user_questions_evaluated)
                return HttpResponse(json.dumps({"url": exam.get_evaluated_url()}))

            messages.error(
                request,
                "If this exam could not be evaluated, please contact the administrator.",
            )
            return redirect(exam.content.get_home_url())

        messages.error(
            request, "the exam does not exist, please contact the administrator."
        )
        return redirect(exam.content.get_home_url())


class examEvaluatedView(ExamsViewFunctions, View):
    template_name = "exams/examEvaluatedView.html"

    def get(self, request, id=None, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("pages:login-page")
        exam = self.get_exam_instance()
        if exam is not None:

            try:
                relation = ExamUserRelations.objects.get(
                    user=self.request.user, exam=exam
                )
                user_questions_evaluated = relation.get_user_answer()
                return render(
                    request,
                    self.template_name,
                    {
                        "relation": relation,
                        "relation_questions": user_questions_evaluated,
                    },
                )
            except ExamUserRelations.DoesNotExist:
                messages.error(
                    request,
                    "there is no relationship between the user and the exam, please contact the admin.",
                )
                return redirect(exam.content.get_home_url())

        messages.error(request, "the exam does not exist, please contact the admin.")
        return redirect(exam.content.get_home_url())

    def post(self, request, *args, **kwargs):
        return redirect("pages:home-page")

