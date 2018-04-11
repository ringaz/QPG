from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Papers(models.Model):
    name = models.CharField(max_length=50)
    paper = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=15, null=True, blank=True)
    level = models.CharField(max_length=15, null=True, blank=True)
    total_marks = models.IntegerField(null=True, blank=True)
    duration = models.CharField(max_length=15, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("paper_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Papers'