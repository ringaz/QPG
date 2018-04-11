from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from questions.models import Subject, Level



# User Profile
class CommonInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    birth_date = models.DateField(verbose_name='date of birth', null=True, blank=True)
    profilepic = models.ImageField(verbose_name='Profile Picture', upload_to='profilepics/', null=True, blank=True)
    address = models.CharField(max_length=30, verbose_name='Physical Address', null=True, blank=True)
    cell = models.IntegerField(null=True, blank=True)
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(max_length=1, choices=GENDER, null=True, blank=True)


    class Meta:
        abstract = True


class Company(CommonInfo):
    company_name = models.CharField(max_length=15, null=True, blank=True)
    company_adress = models.CharField(max_length=15, null=True, blank=True)
    company_cell =models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.company_name


# Save Admin User Signal
@receiver(post_save, sender=User)
def create_or_update_user_company(sender, instance, created, **kwargs):
    if created:
        Company.objects.create(user=instance)
    instance.company.save()

class Teacher(CommonInfo):
    subjects = models.ManyToManyField(Subject)
    levels = models.ManyToManyField(Level)

    def __str__(self):
        return self.user.first_name

# Save Teacher User Signal
@receiver(post_save, sender=User)
def create_or_update_user_teacher(sender, instance, created, **kwargs):
    if created:
        Teacher.objects.create(user=instance)
    instance.teacher.save()



class Recipients(models.Model):
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    email      = models.EmailField()
    subject    = models.CharField(max_length=50)
    level      = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name

