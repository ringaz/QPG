
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import JsonResponse

import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa


from questions.models import Questions
from .models import Papers
from .forms import PaperForm
from questions.filters import QuestionFilter


def ajax_paper_create_view(request):
    response_data = dict()
    if request.method == 'POST':
        name = request.POST.get('name')
        paper = request.POST.get('paper')

        qpaper = Papers.objects.create(name=name, paper=paper, user=request.user)


        response_data['name'] = qpaper.name
        response_data['paper'] = qpaper.paper


        return JsonResponse(response_data)

def ajax_paper_edit_view(request):
    response_data = dict()
    if request.method == 'POST':
        qp_id = request.POST.get('id')
        name = request.POST.get('name')
        paper = request.POST.get('paper')

        Papers.objects.filter(pk=qp_id).update(name=name, paper=paper)

        return JsonResponse(response_data)



def paper_create_view(request):
    question_filter = QuestionFilter(request.GET, queryset=Questions.objects.all())
    question_list_obj = Questions.objects.all()
    paper_form = PaperForm(request.POST or None, request.FILES or None)

    context = {
        "question_filter": question_filter,
        "question_list_obj": question_list_obj,
        "paper_form": paper_form
    }
    return render(request, "papers/generator.html", context)

def paper_edit_view(request, pk):
    instance = get_object_or_404(Papers, pk=pk )
    question_filter = QuestionFilter(request.GET, queryset=Questions.objects.all())
    question_list_obj = Questions.objects.all()
    paper_form = PaperForm(request.POST or None, request.FILES or None, instance=instance)


    context = {
        "qpaper_id": instance.pk,
        "qpaper": instance.paper,
        "question_filter": question_filter,
        "question_list_obj": question_list_obj,
        "paper_form": paper_form
    }
    return render(request, "papers/edit_generator.html", context)


"""
class PaperCreateView(CreateView):
    model = Papers
    form_class = PaperForm
    template_name = 'papers/generator.html'
    success_url = reverse_lazy('paper_list')

    def get_context_data(self, **kwargs):
        question_list_obj = Questions.objects.all()
        kwargs['question_list_obj'] = question_list_obj
        return super().get_context_data(**kwargs)



class PaperUpdateView(UpdateView):
    model = Papers
    form_class = PaperForm
    template_name = 'papers/edit_generator.html'
    success_url = reverse_lazy('paper_list')


"""


class PaperDeleteView(DeleteView):
    model = Papers
    template_name = 'papers/form_delete.html'
    success_url = reverse_lazy('paper_list')


class PaperListView(ListView):
    model = Papers
    template_name = 'papers/list.html'
    context_object_name = 'paper_list_obj'



class PaperDetailView(DetailView):
    model = Papers
    template_name = 'papers/detail.html'
    context_object_name = 'paper_detail_obj'





def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path



def render_pdf_view(request):
    template_path = 'demo.html'
    context = {'name': 'Kelvin Maringire'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
