from django.contrib import admin

from .models import Questions, Subject, Level, Chapter

admin.site.register(Questions)
admin.site.register(Subject)
admin.site.register(Level)
admin.site.register(Chapter)
