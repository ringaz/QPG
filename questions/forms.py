from django import forms

from .models import Questions, Subject, Level, Chapter


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Questions
        fields = [
            'question',
            'answer',
            'subject',
            'level',
            'chapter',
            'marks',
            'question_type',
            'difficulty',
        ]

