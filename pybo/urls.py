from django.urls import path
from .views import base_views, question_views, answer_views

app_name = 'pybo'

urlpatterns = [
    path('', base_views.index, name = 'index'), #view를 인덱스를 호출하겠다는 뜻.
    path('<int:question_id>/', base_views.detail, name = 'detail'), #전달하는 함수를 views.detail 여기 넣어준다.
    path('question/create/', question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', question_views.question_modify, name = 'question_modify'),
    path('question/delete/<int:question_id>/', question_views.question_delete, name = 'question_delete'),
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name = 'answer_modify'),
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name = 'answer_delete'),
]