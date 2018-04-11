from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import JsonResponse
from .models import Questions, Chapter
from .forms import QuestionForm
from .filters import QuestionFilter






def question_list(request):
    question_list_obj = Questions.objects.all()
    return render(request, 'questions/question_list.html', {'question_list_obj': question_list_obj})


def save_question_form(request, form, template_name):
    form.fields["chapter"].queryset = Chapter.objects.none()
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            question_list_obj = Questions.objects.all()
            data['html_question_list'] = render_to_string('questions/includes/partial_question_list.html', {
                'question_list_obj': question_list_obj
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def load_chapters(request):
    subject_id = request.GET.get('subject')
    level_id = request.GET.get('level')
    chapters = Chapter.objects.filter(subject_id=subject_id, level_id=level_id)
    return render(request, 'questions/chapter_dropdown.html', {'chapters': chapters})


def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

    else:
        form = QuestionForm()
    return save_question_form(request, form, 'questions/includes/partial_question_create.html')


def question_update(request, pk):
    question = get_object_or_404(Questions, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
    else:
        form = QuestionForm(instance=question)
    return save_question_form(request, form, 'questions/includes/partial_question_update.html')


def question_delete(request, pk):
    question = get_object_or_404(Questions, pk=pk)
    data = dict()
    if request.method == 'POST':
        question.delete()
        data['form_is_valid'] = True
        question_list_obj = Questions.objects.all()
        data['html_question_list'] = render_to_string('questions/includes/partial_question_list.html', {
            'question_list_obj': question_list_obj
        })
    else:
        context = {'question': question}
        data['html_form'] = render_to_string('questions/includes/partial_question_delete.html', context, request=request)
    return JsonResponse(data)




class QuestionDetailView(DetailView):
    model = Questions
    template_name = 'questions/detail.html'
    context_object_name = 'question_detail_obj'


def search(request):
    question_filter = QuestionFilter(request.GET, queryset=Questions.objects.all())
    return render(request, 'search.html', {'question_filter': question_filter})


"""
def question_create_view(request):
    question_list_obj = Questions.objects.all()
    form = QuestionForm(request.POST or None)
    form.fields["chapter"].queryset = Chapter.objects.none()
    if form.is_valid():
        form.save()
        return redirect('question_list')


    context = {
        "form": form,
        "question_list_obj": question_list_obj
    }
    return render(request, "questions/question_form.html", context)



class QuestionListView(ListView):
    model = Questions
    template_name = 'questions/list.html'
    context_object_name = 'question_list_obj'

class QuestionUpdateView(UpdateView):
    model = Questions
    form_class = QuestionForm
    template_name = 'questions/question_form.html'
    success_url = reverse_lazy('question_list')

class QuestionDeleteView(DeleteView):
    model = Questions
    success_url = reverse_lazy('question_list')
    template_name = 'questions/form_delete.html'




"""











