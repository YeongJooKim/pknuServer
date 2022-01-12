from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#질문 모델을 하나 만들 것이다. 이렇게 질문에 대한 class를 만들었다.
class Question(models.Model): #Model이 부모 클래스가 되는거고 #내가 만든 클래스인 Question에 하나 만들겠다는 뜻.
    subject = models.CharField(max_length=200) #필드에 대한 타입을 적어줘야함. 제목, 내용, 날짜를 씀.
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #User가 죽으면 얘도 같이 죽겠다는 뜻.

    def __str__(self):
        return self.subject

class Answer(models.Model): #Answer에 대한 class를 만듬.
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #외래키는 특정 필드와 연결이 됬을때씀, 괄호 안에는 모델을 삭제할때 여기도 삭제하겠다는 뜻.
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True) #안에 값이 없어도, 공백이어도 값을 허용하겠다는 뜻
    author = models.ForeignKey(User, on_delete=models.CASCADE)