from .models import *
from django.urls import reverse
from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    ##output = '.'.join({q.question_text for q in latest_question_list})
    context = {'questions': latest_question_list}
    return render(request, 'polls/index.html', context) ##HttpResponse(output)

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question': question}) 

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'quesiton': question, 'error_message': f"선택이 없습니다. id={request.POST['choice']}"})
    else:
        # A서버에서도 votes = 1
        # B서버에서도 votes = 1
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))
    
def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question':question})