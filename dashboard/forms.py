from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from import_export import resources

from .models import Company, Teacher, Recipients

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect passsword")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2'

        ]

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = [
            'cell',
            'address',
            'company_name',
            'company_adress',
            'company_cell'
        ]

class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = [
            'cell',
            'address',
            'subjects',
            'levels',
        ]




class RecipientsResource(resources.ModelResource):

    class Meta:
        model = Recipients