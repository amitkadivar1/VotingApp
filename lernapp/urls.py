from django.urls import path
from . import views
app_name='lernapp'
urlpatterns =[
    path('',views.index,name='index'),
    path('userdetail/',views.userdetail,name='userdetail'),
    path('<int:question_id>/userdetail/',views.userquedetail,name='userquedetail'),
    path('<int:question_id>/deletequestion/',views.delete_question,name='deletequestion'),
    path('<int:choice_id>/deletechoice/',views.delete_choice,name='deletechoice'),
    path('<int:question_id>/detail/',views.detail,name='detail'),
    path('<int:question_id>/vote/',views.vote,name='vote'),
    path('<int:question_id>/results/',views.results,name='results'),
    path('<int:question_id>/choiceform/',views.choiceform,name='choiceform'),
    path('<int:question_id>/addchoice/',views.addchoice,name='addchoice'),
    path('search/',views.search,name='search'),
    path('questionform',views.questionform,name="questionform"),
    path('createquestion',views.createquestion,name="createquestion"),
    path('contact/',views.contact,name='contact'),
    path('login/',views.login_page,name='login'),
    path('register/',views.registration_page,name='register'),
    path('logout/',views.logout_page,name='logout'),
]
