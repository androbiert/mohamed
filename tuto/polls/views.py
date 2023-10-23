from django.shortcuts import render,HttpResponse,get_object_or_404,HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from .models import Question,Choice
from .forms import ChoiceSuggestionForm,QuestionForm

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
   
    if request.method=='POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            new_question = form.save()
            return HttpResponseRedirect(reverse('polls:details',args=(new_question.id,)))
    else:
        form = QuestionForm()
    context = {'latest_question_list':latest_question_list,'form':form}
    return render(request,'index.html',context)


def delete_question(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    if request.method == 'POST':
        question.delete()
        return HttpResponseRedirect(reverse('polls:index'),)
    
    
def details(request,question_id):
    try:
         question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("question does not exist !")
    
    if request.method == 'POST':
        form = ChoiceSuggestionForm(request.POST)
        if form.is_valid():
            new_choice= form.save(commit=False)
            new_choice.question = question
            if not question.choice_set.filter(choice_text=new_choice.choice_text).exists():
                new_choice.save()  
            return HttpResponseRedirect(reverse('polls:details',args=(question.id,)))
    else:
        form = ChoiceSuggestionForm()
    
    context = {'question':question,'form':form}
    
    return render(request,'details.html',context)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()
    total = sum(choice.votes for choice in choices)
    for choice in choices:
        if total>0 :
          choice.percentage = (choice.votes / total * 100)
        else:
          choice.percentage = 0
            
    context = {
        'question': question,
        'choices': choices,
    }

    return render(request, 'results.html', context)



def votes(request,question_id):
    question = get_object_or_404(Question,pk= question_id)
    try:
        selected_choice = question.choice_set.get(pk= request.POST['choice']) 
    except(KeyError,Choice.DoesNotExist):
        context = {'question':question ,
                   'error_message':'you did not select a choice please try again !',
                    'form': ChoiceSuggestionForm()}
        return render(request,'details.html',context)
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))
# Create your views here.

