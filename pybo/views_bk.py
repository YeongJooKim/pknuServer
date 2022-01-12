from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer  # 내가 모델 파일의 Question 내용을 import(참고) 하겠다는 뜻.
from django.utils import timezone  # 언제 등록했는지 시간을 등록할때 timezone이 필요함.
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# from django.http import HttpResponse

# Create your views here.
def index(request):
    """
    질문 목록 출력
    """

    page = request.GET.get('page', '1')

    question_list = Question.objects.order_by('-create_date')  # Question의 목록을 가져오겠다. order_by = 정렬을 하겠다.

    # 페이징 처리 - 공식처럼 다른 곳에서도 이렇게 똑같은 코드가 쓰인다.
    paginator = Paginator(question_list, 10)  # 페이지에서 글을 10개씩 잘라서 보이게 하겠다.
    page_obj = paginator.get_page(page)

    # Question_list 이렇게 받아서 넘겨주겠다. 이 객체 안에 질문들이 다 들어가있다.

    context = {'question_list': page_obj}  # 앞에 있는게 key, 뒤에있는데 value이다. dictionary 객체 내부에 키밸류 형태로 저장이 되어 있다.
    return render(request, 'pybo/question_list.html', context)  # 얘는 데이터를 받아서 렌더링해줄수있는 함수이다.
    # 세번째의 context를 중앙에서 보내주겠다는 뜻. 템플릿 파일을 만들어서 그 안에 내용을 넣을 예정임.


#    return HttpResponse("Hello World")

def detail(request, question_id):
    """
    질문 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)  # pk라는 속성이 안에 내장되어 있다.
    context = {'question': question}  # {key, value} 형태로 context로 받음.
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    답변 등록
    """
    question = get_object_or_404(Question, pk = question_id)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id = question.id)
    else:
        form = AnswerForm()

    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

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

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    답변 수정
    """
    answer = get_object_or_404(Answer, pk = answer_id)
    if request.user != answer.author: #글쓴이랑 사용자가 같지 않다면 수정할수없다고 에러 메시지를 보내라
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id = answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer) #instance는 os 내부에서 다른 것끼리 차이를 구분하는 키(열쇠)같은 것이다.
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id = answer.question.id)
    else:
        form = AnswerForm(instance=answer)

    context = {'answer' : answer, 'form' : form}
    return render(request, 'pybo/answer_form.html', context) #결국엔 question_form으로 간다.


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    답변 삭제
    """
    answer = get_object_or_404(Answer, pk = answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다.')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id = answer.question.id)