from django.urls import path
from . import views
app_name='lernapp'
urlpatterns =[
    path('index/',views.index,name='index'),
    path('<int:question_id>/detail/',views.detail,name='detail'),
    path('<int:question_id>/vote/',views.vote,name='vote'),
    path('<int:question_id>/results/',views.results,name='results'),
    path('<int:question_id>/choiceform/',views.choiceform,name='choiceform'),
    path('<int:question_id>/addchoice/',views.addchoice,name='addchoice'),
    path('search/',views.search,name='search'),
    path('questionform',views.questionform,name="questionform"),
    path('createquestion',views.createquestion,name="createquestion"),
]
