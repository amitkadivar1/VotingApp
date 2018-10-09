import datetime
from django.conf import settings
from django.utils import timezone
from django.db import models
# Create your models here.
User=settings.AUTH_USER_MODEL
class Login(models.Model):
    username=models.CharField(max_length=255)
    session_name=models.BooleanField(default=False)
class Question(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    question_text=models.CharField(max_length=255)
    # choice=models.ManyToManyField(Choice)
    pub_date=models.DateTimeField('date published')
    count=models.IntegerField(default=0)


    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text=models.CharField(max_length=255)
    votes=models.IntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.choice_text)
#
# class User(models.Model):
#     user=models.CharField(max_length=20)
#     # question=models.ForeignKey(Question,on_delete=models.CASCADE)
#     def __str__(self):
#         return self.user
#         # return "(User: {}) (QUESTION: {}) (Count: {})".format(self.user,self.question,self.count)

class UserVote(models.Model):
    user        = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    question    = models.ForeignKey(Question,on_delete=models.CASCADE)
    choice      = models.ForeignKey(Choice,on_delete=models.CASCADE)
    count       = models.IntegerField(default=0)
    votes       =models.IntegerField(default=0)
    def __str__(self):
        return '{}'.format(self.user)
