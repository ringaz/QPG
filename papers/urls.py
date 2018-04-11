from django.urls import path

from .views import (
    #PaperUpdateView,
    PaperDeleteView,
    PaperListView,
    PaperDetailView,
    paper_create_view,
    paper_edit_view,
    ajax_paper_create_view,
    ajax_paper_edit_view,
    render_pdf_view
)

urlpatterns = [
    # Papers
    path('', PaperListView.as_view(), name='paper_list'),
    path('<int:pk>/', PaperDetailView.as_view(), name='paper_detail'),
    path('create/', paper_create_view, name='paper_create'),
    path('<int:pk>/edit/', paper_edit_view, name='paper_edit'),
    path('<int:pk>/delete/', PaperDeleteView.as_view(), name='paper_delete'),
    path('ajax_create/', ajax_paper_create_view, name='ajax_create'),
    path('ajax_edit/', ajax_paper_edit_view, name='ajax_edit'),
    path('pdf/', render_pdf_view, name='pdf'),


]

