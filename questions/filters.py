import django_filters

from django import forms

from .models import Questions


QuestionType = (
        (None, '--------'),
        ('M', 'Multiple Choice'),
        ('F', 'Essay'),
    )
Difficulty = (
        (None, '--------'),
        ('M', 'Easy'),
        ('M', 'Intermidiate'),
        ('F', 'Hard'),
    )

class QuestionFilter(django_filters.FilterSet):
    question = django_filters.CharFilter(lookup_expr='icontains')
    subject = django_filters.CharFilter(lookup_expr='icontains')
    level = django_filters.CharFilter(lookup_expr='icontains')
    chapter = django_filters.CharFilter(lookup_expr='icontains')
    question_type = django_filters.ChoiceFilter(choices=QuestionType)
    difficulty = django_filters.ChoiceFilter(choices=Difficulty)

    class Meta:
        model = Questions
        fields = [
            'question',
            'subject',
            'level',
            'chapter',
            'marks',
            'question_type',
            'difficulty',
        ]