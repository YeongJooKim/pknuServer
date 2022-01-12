from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone  # 언제 등록했는지 시간을 등록할때 timezone이 필요함.

from ..forms import QuestionForm
from ..models import Question  # 내가 모델 파일의 Question 내용을 import(참고) 하겠다는 뜻.


@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문 등록 #여기서 질문 등록을 누르면 이제 등록하고 저장할수있게 된다. 여기서 질문을 등록하면 전부 db에 저장이 된다.
    """
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)  # 질문 등록에서 현재 내가 입력한 내용들을 save하고 'pybo:index'를 호출하게됨.
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')

    else:
        form = QuestionForm()  # UI를 나오게 만들어야 함. form = 객체 - 보여줘야한다.

    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    질문 수정
    """
    question = get_object_or_404(Question, pk = question_id)
    if request.user != question.author: #글쓴이랑 사용자가 같지 않다면 수정할수없다고 에러 메시지를 보내라
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id = question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question) #instance는 os 내부에서 다른 것끼리 차이를 구분하는 키(열쇠)같은 것이다.
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id = question.id)
    else:
        form = QuestionForm(instance=question)

    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context) #결국엔 question_form으로 간다.

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:  # 글쓴이랑 사용자가 같지 않다면 수정할수없다고 에러 메시지를 보내라
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)

    question.delete()
    return redirect('pybo:index')
