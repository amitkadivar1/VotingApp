from django.contrib import admin
from .models import Question,Choice,UserVote,Login
# Register your models here.
class UserModel(admin.ModelAdmin):
    list_display=('question','user','votes')
admin.site.register(Question)
admin.site.register(Choice)
# admin.site.register(User)
admin.site.register(UserVote,UserModel)
admin.site.register(Login)
