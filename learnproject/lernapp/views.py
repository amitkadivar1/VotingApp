from django.shortcuts import render,get_object_or_404,reverse
from django.http import HttpResponse,HttpResponseRedirect
from .models import Choice,Question
from django.utils import timezone
import datetime
# Create your views here.
def index(request):
    question=Question.objects.all
    return render(request,'learnapp/home.html',{'question':question})



def detail(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    choice=question.choice_set.all
    return render(request,'learnapp/detail.html',{'choice':choice,'question':question})


def vote(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    choice=question.choice_set.all()
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'learnapp/detail.html',{
                                                    'question':question,
                                                    'choice':choice,
                                                    'error_message':"you're not selected any choice",
                                                     })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('lernapp:results', args=(question.id,)))


def results(request,question_id):
    question=get_object_or_404(Question, pk=question_id)
    return render(request,'learnapp/results.html',{'question':question})

def choiceform(request,question_id):
    question=Question.objects.get(pk=question_id)
    return render(request,'learnapp/createchoice.html',{'question':question})

def addchoice(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    print(question)c
    if request.method == 'POST':
        choice_text=request.POST.get('choice')
        createchoice=question.choice_set.create(choice_text=choice_text,votes=0)

    return render(request, 'learnapp/detail.html', {'question':question})


def search(request):
    if request.method =='POST':
        search=request.POST.get('search')
        print(search)
        search_filter=Question.objects.filter(question_text__startswith=search ,question_text__endswith=search)
        # if search_filter[0]==None:
        #     search_filter=Question.objects.filter(question_text__endswith=search)
        #     print(search_filter[0])
        # print(search_filter[0])

        return render(request,'learnapp/search.html',{'search_filter':search_filter,'search':search})
    else:
        print("not post ")
def questionform(request):
    return render(request,'learnapp/createquestion.html',{})

def createquestion(request):
    if request.method == "POST":
        list=[]
        get_new_question=request.POST.get('newquestion',None)
        print(get_new_question)
        questions=Question.objects.all()
        new_question=Question(question_text=get_new_question,pub_date=timezone.now())
        new_question.save()
        question=Question.objects.all()
        error_message="succefuly add question"
        context={'question':question,'error_message':error_message,}

        # for question in questions:
        #     list.append(question.question_text)
        # print(list)
        # if  get_new_question in list:
        #     print(question.question_text)
        #     question=Question.objects.all()
        #     error_message="same question already avilable "
        #     context={
        #     'question':question,
        #     'error_message':error_message,
        #     }
        # else:
        #     print(question.question_text)
        #     print('else')
        #     new_question=Question(question_text=get_new_question,pub_date=timezone.now())
        #     new_question.save()
        #     question=Question.objects.all()
        #     error_message="succefuly add question"
        #     context={'question':question,'error_message':error_message,}

        return render(request,'learnapp/home.html',context)
