from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from courses.models import Content
from django.utils import timezone
from django.urls import reverse
from operator import itemgetter
from users.models import User
from django.db import models
import ast


class Exam(models.Model):

    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    content = models.OneToOneField(
        Content, blank=True, null=True, default=None, on_delete=models.SET_DEFAULT
    )
    name = models.CharField(
        ("Exam name"),
        max_length=150,
        unique=False,
        blank=False,
        help_text=("Required. 150 characters or fewer."),
    )
    description = models.TextField()
    approved = models.DecimalField(
        ("minimun points to approved"),
        default=None,
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
        help_text=(
            "Put here the minimum points necessary to pass this exam. Max 5 digits: 3 for en integer part and 2 for decimal part"
        ),
        error_messages={
            "blank": ("you must provied the minimun points."),
            "null": ("you must provied the minimun points."),
        },
    )
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Quiz: " + self.name

    def save(self, *args, **kwargs):
        questionlistForms = kwargs.pop("questionlist", None)
        if kwargs.pop("update", None):
            Question.objects.filter(exam=self).delete()
        super(Exam, self).save(*args, **kwargs)
        if questionlistForms:
            for questionForm in questionlistForms:
                question_instance = questionForm.save(commit=False)
                question_instance.exam = self
                question_instance.save(
                    answerlist=questionForm.answersForms(),
                    familyInstance={"Exam": self},
                )

    def get_owner(self):
        return self.user.get_full_name()

    def get_questions_instances(self):
        questions = Question.objects.filter(exam=self)
        numbers_of_questions = [index + 1 for index in range(questions.count())]

        return zip(numbers_of_questions, questions)

    def get_take_url(self):
        # return reverse("courses:course-home-week-content", kwargs={'id':self.course.id, 'idModule':self.module.id, 'idContent':self.id})
        # return reverse("exams:exam-take", kwargs={'id':self.content.belongs_to_the_course().id, 'idModule':self.content.belongs_to_the_module().id, 'idContent':self.content.id, 'idExam':self.id})
        return reverse("exams:exam-take", kwargs={"idExam": self.id})

    def get_detail_url(self):
        return reverse("exams:exam-detail", kwargs={"id": self.id})

    def get_edit_url(self):
        return reverse("exams:exam-update", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("exams:exam-delete", kwargs={"id": self.id})

    def get_evaluated_url(self):
        return reverse("exams:exam-evaluated", kwargs={"idExam": self.id})

    def evaluate(self, questions):
        if not questions:
            raise "they must provide the questions with their answers to evaluate"
        for question in questions.values():
            question["Answers"] = sorted(question["Answers"], key=itemgetter(0))
        questions_instances = [
            question for _, question in self.get_questions_instances()
        ]
        if len(questions_instances) != len(questions):
            raise "must provide all questions associated with this exam"
        validation = {}
        for question_instance, question in zip(questions_instances, questions.values()):
            validation["Questionid"] = question_instance.id
            answers_instances = question_instance.get_answers_instances()
            if len(answers_instances) != len(question["Answers"]):
                raise "must provide all answers associated with this exam"
            question["validate"] = True
            for answer_instance, answer in zip(answers_instances, question["Answers"]):
                if answer_instance.correct_answer != answer[1]:
                    question["validate"] = False
                    continue
            del question["Answers"]
            question["points"] = (
                float(question_instance.question_value)
                if question["validate"]
                else float(0)
            )
        questions["approved"] = float(self.approved)
        return questions


class Question(models.Model):
    exam = models.ForeignKey(Exam, default=None, on_delete=models.CASCADE)
    question = models.CharField(
        ("question"),
        max_length=600,
        blank=False,
        unique=False,
        help_text=("Required. 600 characters or fewer."),
        error_messages={"unique": ("A question with that name already exists."),},
    )
    correct_answers = models.IntegerField(
        ("number of correct answers for this question"),
        help_text=("number of correct answers for this question"),
        default=0,
    )
    question_value = models.DecimalField(
        ("points"),
        default=None,
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text=('Max 5 digits: same as "minimun points to approved"'),
        # help_text=('point value of the question. Max 5 digits: 3 for en integer part and 2 for decimal part'),
        blank=False,
        null=False,
        error_messages={
            "blank": ("you must provied the point value."),
            "null": ("you must provied the point value."),
        },
    )

    def __str__(self):
        return "Question: " + self.question

    def save(self, *args, **kwargs):
        answerlistForms = kwargs.pop("answerlist", None)
        familyInstance = kwargs.pop("familyInstance", None)
        super(Question, self).save(*args, **kwargs)
        if answerlistForms:
            for answerForm in answerlistForms:
                answer_instance = answerForm.save(commit=False)
                answer_instance.exam = familyInstance["Exam"]
                answer_instance.question = self
                answer_instance.save()

    def get_answers_instances(self):
        return Answer.objects.filter(question=self)

    def get_altAnswers_instances(self):
        return Answer.objects.filter(question=self).order_by("?")


class Answer(models.Model):
    exam = models.ForeignKey(Exam, default=None, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, default=None, on_delete=models.CASCADE)
    answer = models.CharField(("answer"), max_length=600, blank=False,)
    correct_answer = models.BooleanField(
        default=False, help_text=("the answer is correct?."),
    )

    def __str__(self):
        return "answer for question, " + str(self.question_id)


class ExamUserRelations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user_answer = models.TextField(default=None, blank=True, null=True)
    points = models.DecimalField(
        default=0,
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    number_of_try = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(3)]
    )
    last_try = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return self.exam.name + ": " + self.user.get_full_name()

    def can_take_exam(self):
        if self.number_of_try >= 3:
            if self.time().days > 0 or self.time().seconds > (8 * 60 * 60):
                self.number_of_try = 0
                self.save()
                return True
            return False
        return True

    def get_user_answer(self):
        user_answer = ast.literal_eval(self.user_answer)
        del user_answer["approved"]
        for question in user_answer.values():
            question["id"] = int(question["id"])
        return user_answer

    def time(self):
        return timezone.now() - self.last_try

    def time_until_take(self):
        time = (
            timezone.timedelta(days=0, seconds=8 * 60 * 60, microseconds=0)
            - self.time()
        )
        return "%s hour(s) and %s minut(s)" % (
            time.seconds // 3600,
            (time.seconds // 60) % 60,
        )

    def try_exam(self, userQuestions):
        self.number_of_try += 1
        self.last_try = timezone.now()
        self.user_answer = userQuestions
        new_points = 0
        for key, question in userQuestions.items():
            if key != "approved":
                new_points += question["points"]
        if new_points > self.points:
            self.points = new_points
        self.save()
