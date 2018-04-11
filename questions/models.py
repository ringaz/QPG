from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class Subject(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    name = models.CharField(max_length=30)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    level = models.ManyToManyField(Level, blank=True)

    def __str__(self):
        return self.name

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

class Questions(models.Model):
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, max_length=15, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True)
    marks = models.IntegerField(null=True, blank=True)
    question_type = models.CharField(max_length=1, choices=QuestionType, null=True, blank=True)
    difficulty = models.CharField(max_length=1, choices=Difficulty, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = 'Questions'


