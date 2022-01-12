from django import forms
from pybo.models import Question, Answer #Question, Answer 이라는 내용을 밑에 형식에 집어 넣은 것이다.

class QuestionForm(forms.ModelForm): #모델과 관련된 폼이라고 생각하기. 우리가 만든 모델에서 어떠한 일을 할것이다.
    class Meta: #Meta 클래스라는 것은 하나의 형식이라고 보면 된다. 모델 폼을 상속을 받았을때 반드시 필요하다.
        model = Question
        fields = ['subject', 'content'] #Question에서 가져온 'subject', 'content' 두개를 사용한다.

        labels = {
            'subject': '제목',
            'content': '내용',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer #Answer객체를 model에 넣어주고
        fields = ['content'] #이 안에는 content만 남겨두면 될 것 같다. 제목은 필요없음

        labels = {
            'content': '답변 내용',
        }