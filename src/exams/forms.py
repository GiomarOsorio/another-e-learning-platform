from django import forms
from .models import (
    Exam,
    Question,
    Answer,
)

# Relate to the answers
class AnswerCreate(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            "answer",
            "correct_answer",
        ]

    field_order = [
        "answer",
        "correct_answer",
    ]


# Relate to the questions
class QuestionCreate(forms.ModelForm):
    answerlist = []

    class Meta:
        model = Question
        fields = [
            "question",
            "correct_answers",
            "question_value",
        ]

    def __init__(self, *args, **kwargs):
        answers = kwargs.pop("answers", None)
        super(QuestionCreate, self).__init__(*args, **kwargs)
        if answers:
            self.answerlist = []
            for iAnswer in answers:
                self.answerlist.append(AnswerCreate(answers[iAnswer]))

    def is_valid(self):
        """Return True if the form has no errors, or False otherwise."""
        if self.is_bound and not self.errors:
            valid = True
        else:
            return False
        for answerForm in self.answerlist:
            if not answerForm.is_valid():
                valid = False
        return valid

    def answersForms(self):
        return self.answerlist


# related to the quizzes
class ExamCreate(forms.ModelForm):
    questionTemplate = QuestionCreate()
    answerTemplate = AnswerCreate()
    questionlist = []

    class Meta:
        model = Exam
        fields = ["name", "description", "approved"]

    def __init__(self, *args, **kwargs):
        questions = kwargs.pop("questions", None)
        super(ExamCreate, self).__init__(*args, **kwargs)
        if questions:
            self.questionlist = []
            for iQuestion in questions:
                answersData = questions[iQuestion].pop("Answers")
                self.questionlist.append(
                    QuestionCreate(questions[iQuestion], answers=answersData)
                )

    def is_valid(self):
        """Return True if the form has no errors, or False otherwise."""
        if self.is_bound and not self.errors:
            valid = True
        else:
            return False
        for questionForm in self.questionlist:
            if not questionForm.is_valid():
                valid = False
        return valid

    def has_children_forms(self):
        return False if len(self.questionlist) == 0 else True

    def questions_forms(self):
        return self.questionlist

    # def get_question_template(self):
    #     return self.questionTemplate

    # def getAnswerTemplate(self):
    #     return self.answerTemplate

