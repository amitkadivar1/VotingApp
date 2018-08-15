from django.shortcuts import render,get_object_or_404,reverse,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,get_user_model,logout
from .forms import ContactForm,LoginForm,RegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Choice,Question
from django.utils import timezone
import datetime
# Create your views here.
@login_required(login_url='/login')
def index(request):
    question=Question.objects.all
    return render(request,'learnapp/home.html',{'question':question})


@login_required(login_url='/login')
def detail(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    choice=question.choice_set.all
    return render(request,'learnapp/detail.html',{'choice':choice,'question':question})

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def results(request,question_id):
    question=get_object_or_404(Question, pk=question_id)
    return render(request,'learnapp/results.html',{'question':question})

@login_required(login_url='/login')
def choiceform(request,question_id):
    question=Question.objects.get(pk=question_id)
    return render(request,'learnapp/createchoice.html',{'question':question})

@login_required(login_url='/login')
def addchoice(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    print(question)
    if request.method == 'POST':
        choice_text=request.POST.get('choice')
        createchoice=question.choice_set.create(choice_text=choice_text,votes=0)

    return render(request, 'learnapp/detail.html', {'question':question})

@login_required(login_url='/login')
def search(request):
    if request.method =='POST':
        search=request.POST.get('search')
        print(search)
        search_filter=Question.objects.filter(question_text__startswith=search)

            # if search_filter[0]==None:
            #     search_filter=Question.objects.filter(question_text__endswith=search)
            #     print(search_filter[0])
            # print(search_filter[0])
        return render(request,'learnapp/search.html',{'search_filter':search_filter,'search':search})
    else:
        print("not post ")
@login_required(login_url='/login')
def questionform(request):
    return render(request,'learnapp/createquestion.html',{})
@login_required(login_url='/login')
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
@login_required(login_url='/login')
def contact(request):
    contactform=ContactForm(request.POST or None)
    content={
        'title':'Contact Form',
        'content':'Welcome to contact page',
        'form':contactform,
    }
    if contactform.is_valid():
        print(contactform.cleaned_data)
    # if request.method =="POST":
    #     print(request.POST.get('name'))
    #     print(request.POST.get('email'))
    #     print(request.POST.get('message'))
    return render(request,'learnapp/contact_form.html',content)

def login_page(request):
    loginform=LoginForm(request.POST or None)
    context={
        'title':"Login Form",
        'form':loginform,
    }

    # print(request.user.is_authenticated)
    if loginform.is_valid():
        print(loginform.cleaned_data)
        username=loginform.cleaned_data.get('username')
        password=loginform.cleaned_data.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            print(request.user.is_authenticated)
            login(request,user)
            # print(request.user.is_authenticated)
            # context['form']=LoginForm()
            return redirect('/index')
        else:
            print('Error')
    return render(request,'learnapp/login.html',context)


user=get_user_model()
def registration_page(request):
    form=RegistrationForm(request.POST or None)
    context={
        'title':'Registration Form',
        'form':form,
    }
    if form.is_valid():
        # print(form.cleaned_data)
        username=form.cleaned_data.get('username')
        email=form.cleaned_data.get('email')
        password=form.cleaned_data.get('password')
        new_user=user.objects.create_user(username,email,password)
        # print(new_user)
        return redirect('/login/')
    else:
        print(form.errors )
    return render(request,'learnapp/registration_page.html',context)
def logout_page(request):
    logout(request)
    return redirect('/login/')
