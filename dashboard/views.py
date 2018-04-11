from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.base import TemplateView, View
from django.contrib.auth.models import User, Group


from .forms import CompanyForm, TeacherForm, UserForm, UserEditForm, UserLoginForm


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect('company_create_view')
        else:
            redirect('login_view')
    return render(request, "dashboard/login.html", {"login_form":form})

def login_vieww(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        redirect('company_create_view')
    else:
        redirect('login_view')
    return render(request, "dashboard/login.html")



def logout_view(request):
    logout(request)
    redirect('login_view')


#Company Register View
def company_create_view(request):
    user_form = UserForm(request.POST or None)
    company_form = CompanyForm(request.POST)
    if user_form.is_valid() and company_form.is_valid():
        user = user_form.save()
        admin = Group.objects.get(name = "Admin")
        user.groups.add(admin)
        user.refresh_from_db()
        user.company.company_name = company_form.cleaned_data.get('company_name')
        user.company.company_adress = company_form.cleaned_data.get('company_adress')
        user.company.company_cell = company_form.cleaned_data.get('company_cell')
        user.company.cell = company_form.cleaned_data.get('cell')
        user.company.address = company_form.cleaned_data.get('address')
        user.save()
        password = user_form.cleaned_data.get('password')
        user.set_password(password)
        user = authenticate(username=user.username, password=password)
        login(request, user)
        return redirect("company_edit_view")

    context = {
        "user_form": user_form,
        "company_form": company_form
    }
    return render(request, "dashboard/company_registration.html", context)


@transaction.atomic
def company_edit_view(request):
    if request.method == 'POST':
        user_edit_form = UserEditForm(request.POST, instance=request.user)
        company_form = CompanyForm(request.POST, instance=request.user.company)
        if user_edit_form.is_valid() and company_form.is_valid():
            user_edit_form.save()
            company_form.save()
            messages.success(request, 'Your profile was successfully updated')
            return redirect("company_edit_view")
        else:
            messages.error(request,'Please correct your error')
    else:
        user_edit_form = UserEditForm(instance=request.user)
        company_form = CompanyForm(instance=request.user.company)

    return render(request, 'dashboard/company_edit.html', {
        'user_edit_form': user_edit_form,
        'company_form': company_form
    })


#Teacher Register View
def teacher_create_view(request):
    user_form = UserForm(request.POST or None)
    teacher_form = TeacherForm(request.POST)
    if user_form.is_valid() and teacher_form.is_valid():
        user = user_form.save()
        teacher = Group.objects.get(name = "Teacher")
        user.groups.add(teacher)
        user.refresh_from_db()
        #user.teacher.subjects = teacher_form.cleaned_data.set('subjects')
        #user.teacher.levels = teacher_form.cleaned_data.set('levels')
        user.teacher.subjects.add(*teacher_form.cleaned_data.get('subjects'))
        user.teacher.levels.add(*teacher_form.cleaned_data.get('levels'))
        user.teacher.cell = teacher_form.cleaned_data.get('cell')
        user.teacher.address = teacher_form.cleaned_data.get('address')
        user.save()
        password = user_form.cleaned_data.get('password')
        user.set_password(password)
        user = authenticate(username=user.username, password=password)
        login(request, user)
        return redirect("teacher_edit_view")

    context = {
        "user_form": user_form,
        "teacher_form": teacher_form
    }
    return render(request, "dashboard/teacher_registration.html", context)


@transaction.atomic
def teacher_edit_view(request):
    if request.method == 'POST':
        user_edit_form = UserEditForm(request.POST, instance=request.user)
        teacher_form = TeacherForm(request.POST, instance=request.user.company)
        if user_edit_form.is_valid() and teacher_form.is_valid():
            user_edit_form.save()
            teacher_form.save()
            messages.success(request, 'Your profile was successfully updated')
            return redirect("teacher_edit_view")
        else:
            messages.error(request,'Please correct your error')
    else:
        user_edit_form = UserEditForm(instance=request.user)
        teacher_form = TeacherForm(instance=request.user.teacher)

    return render(request, 'dashboard/teacher_edit.html', {
        'user_edit_form': user_edit_form,
        'teacher_form': teacher_form
    })



#User List
def users_list(request):
    users = User.objects.all()
    context = {
        'users': users
    }

    return render(request, 'dashboard/userlist.html', context)

class DashboardView(TemplateView):
    template_name = "base.html"

#PasswordChangeView
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dashboard/password_change_form.html', {
        'form': form
    })


dashboard_view = DashboardView.as_view()