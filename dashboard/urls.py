from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .views import  dashboard_view, users_list, change_password, login_view, logout_view, company_create_view, company_edit_view, teacher_create_view, teacher_edit_view

urlpatterns = [
    #Homepage
    path('home/', TemplateView.as_view(template_name='dashboard/homepage.html'), name='home' ),
    #Authentication
    path('login/', login_view, name ='login_view'),
    path('logout/', logout_view, name ='logout_view'),
    path('register/', company_create_view, name ='company_create_view'),
    path('company_edit/', company_edit_view, name ='company_edit_view'),
    path('teacher_create/', teacher_create_view, name ='teacher_create_view'),
    path('teacher_edit/', teacher_edit_view, name ='teacher_edit_view'),
    #Dashboard
    path('dashboard/', dashboard_view, name = 'dashboard' ),
    #user list
    path('userlist/', users_list, name='userlist'),
    #Password Change
    path('password_change/', change_password, name='change_password'),
    #Password Reset
    path('password_reset/', auth_views.password_reset, name='password_reset'),
    path('password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),


]