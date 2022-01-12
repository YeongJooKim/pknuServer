from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm

def signup(request):
    """
    계정 생성
    """
    if request.method == "POST": #만약 현재 요청한 방법이 포스트 방법이라면
        form = UserForm(request.POST)
        if form.is_valid():
            form.save() #form이 유효하다면 save하고
            username = form.cleaned_data.get('username') #사용자의 아이디와 비밀번호를 얻기위해
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password) #사용자 인증
            login(request, user) #login했을때 user 값을 넣어준다.
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form' : form}) #form 객체로 넘겨주겠다.