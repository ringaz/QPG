from django.contrib import admin
from .models import Company, Teacher, Recipients
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from .forms import RecipientsResource


admin.site.register(Company)
admin.site.register(Teacher)


class RecipientsAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    resource_class = RecipientsResource

admin.site.register(Recipients, RecipientsAdmin)