from django.contrib import admin
from .models import Question

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject'] #질문에 대한 검색을 만드는 코드, subject를 등록할수있음

# Register your models here. # 니가 디비에 기록할 answer 데이터가 있으면 여기에 기록하라는 뜻
admin.site.register(Question, QuestionAdmin) # Question 모델을 기록함.