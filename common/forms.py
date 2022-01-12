from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm): #상속하는 이유는 좀 편하게 쓸려고, 이 안에 코드를 넣어두면 알아서 처리가 다 됌.
    email = forms.EmailField(label = "이메일") #이메일 필드를 따로 놓은 이유는 1. 외국에선 회원가입할때 이메일을 반드시 기입함. 2. 따로 관리? 하기위해?

    class Meta:
        model = User #User 객체를 모델에다 넘겨주고
        fields = ("username", "password1", "password2", "email") #회원가입 칸들