from django.shortcuts import render,get_object_or_404,reverse,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,get_user_model,logout
from .forms import ContactForm,LoginForm,RegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Choice,Question,UserVote,Login

from django.contrib import messages

from django.utils import timezone
import datetime
# Create your views here.
@login_required(login_url='/login')
def index(request):
    print(request.session.get("user"))
    question=Question.objects.all()
    return render(request,'learnapp/home.html',{'question':question})
    # else:
    #     return redirect('lernapp:login')


@login_required(login_url='/login')
def detail(request,question_id):
    list=[]
    question=get_object_or_404(Question,pk=question_id)
    uservote=question.uservote_set.all()
    for vote in uservote:
        list.append(vote.user)
    if request.user in list:
        messages.error(request,"You Already give vote for this Question")
        return redirect('lernapp:index')
    else:
        print("2")
        choice=question.choice_set.all()
        return render(request,'learnapp/detail.html',{'choice':choice,'question':question})
@login_required(login_url='/login')
def vote(request,question_id):
    list=[]
    question=get_object_or_404(Question,pk=question_id)
    uservote=question.uservote_set.all()
    choice=question.choice_set.all()
    selected_choice=question.choice_set.get(pk=request.POST['choice'])
    for vote in uservote:
        list.append(vote.user)
    if request.user in list:
        print("Exist")
        return redirect('lernapp:index')
    else:
        try:
            selected_choice=question.choice_set.get(pk=request.POST['choice'])
            print(selected_choice)
        except (KeyError,Choice.DoesNotExist):
            return render(request,'learnapp/detail.html',{'question':question,'choice':choice,'error_message':"you're not selected any choice",
                                                        })
        else:
            print("vote")
            selected_choice.votes += 1
            selected_choice.save()
            selected_choice.user=request.user
            selected_choice.save()
            vote=selected_choice.votes
            print(vote)
            question.count +=1
            question.save()
            count=question.count
            UserVote.objects.create(user=request.user,question=question,choice=selected_choice,votes=vote,count=count)
        # print(selected_choice.user)
            return HttpResponseRedirect(reverse('lernapp:results', args=(question.id,)))


@login_required(login_url='/login')
def results(request,question_id):
    question=get_object_or_404(Question, pk=question_id)
    return render(request,'learnapp/results.html',{'question':question})

@login_required(login_url='/login')
def choiceform(request,question_id):
    question=Question.objects.get(pk=question_id)
    return render(request,'learnapp/createchoice.html',{'question':question})

def delete_choice(request,choice_id):
    choice=get_object_or_404(Choice,pk=choice_id)
    question=choice.question
    print(choice)
    choice.delete()
    return render(request,'learnapp/detail.html',{'choice':choice,'question':question})

def delete_question(request,question_id):
    question_id=get_object_or_404(Question,pk=question_id)
    question_id.delete()
    question=Question.objects.all()

    return render(request,'learnapp/home.html',{'question':question})


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
            request.session['user']=request.user.username
            Login.objects.create(username=request.user,session_name=True)
            return redirect('lernapp:index')
        # elif Login.session_name==True:
        #         return redirect('lernapp:index')
        else:
            messages.error(request,"Enter Detail is wrong please check!!!!")
            return redirect('lernapp:login')
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
        print(form.error)
    return render(request,'learnapp/registration_page.html',context)
@login_required(login_url='/login')
def userdetail(request):
    if request.user.is_staff:
        question=Question.objects.all()
        context={'question':question}
    else:
        print("you are not authenticate person ")
    return render(request,'learnapp/userque.html',context)
@login_required(login_url='/login')
def userquedetail(request,question_id):
    votes=0
    list=[]
    question=get_object_or_404(Question, pk=question_id)
    choice=question.choice_set.all()
    uservote=question.uservote_set.all()
    print(uservote)
    for ch in choice:
        votes+=ch.votes
    for uv in uservote:
        list.append(uv.user)

    if len(list)==0 :
        user="No any user give vote "
        context={
            'question':question,
            'choice':choice,
            'message':user,
        # 'votes':vote
        }
    else:
        totaluser=len(list)
        print(list)
        context={
            'question':question,
            'choice':choice,
            'votes':votes,
            'user':list,
            'totaluser':totaluser,
        # 'votes':vote
        }
    return render(request,'learnapp/userquedetail.html',context)

def logout_page(request):
    logout(request)
    message=messages.success(request,'succefuly logout!!')

    return render(request,'learnapp/logout.html',{'message':message})
