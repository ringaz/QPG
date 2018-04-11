from django.urls import path
from django_filters.views import FilterView
from .filters import QuestionFilter


from .views import (
    #QuestionCreateView,
    #QuestionUpdateView,
    #QuestionDeleteView,
    #QuestionListView,
    QuestionDetailView,
    search,
    #question_create_view,
    load_chapters,
    question_list,
    question_create,
    question_update,
    question_delete



)

urlpatterns = [
    # Questions
    path('', question_list, name='question_list'),
    path('create/', question_create, name='question_create'),
    path('<int:pk>/update/', question_update, name='question_update'),
    path('<int:pk>/delete/', question_delete, name='question_delete'),
    #path('', QuestionListView.as_view(), name='question_list'),
    path('<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    #path('create/', QuestionCreateView.as_view(), name='question_create'),
    #path('create/', question_create_view, name='question_create'),
    #path('<int:pk>/edit/', QuestionUpdateView.as_view(), name='question_edit'),
    #path('<int:pk>/delete/', QuestionDeleteView.as_view(), name='question_delete'),
    #search
    path('search/', search, name='search'),
    #chapter_ajax
    path('load-chapters/', load_chapters, name='load_chapters'),


]