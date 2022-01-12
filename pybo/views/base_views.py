from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from ..models import Question, Answer #.이 하나면 이곳만 적용이 되고 ..이면 그 상위 데이터까지
from django.db.models import Q, Count

# Create your views here.
def index(request):
    """
    질문 목록 출력
    """
    page = request.GET.get('page', '1') #get 방식으로 페이지의 정보를 가져옴
    kw = request.GET.get('kw', '') #검색어를 입력하게되면 그 입력값에 해당하는 keyword를 넘겨줄것이다.
    so = request.GET.get('so', 'recent')

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')  # Question의 목록을 가져오겠다. order_by = 정렬을 하겠다.

    if kw:
        question_list = question_list.filter( #300개의 question list에서 그 kw가 포함이 되어있는지 찾는 필터
            Q(subject__icontains=kw) | #이건 문법이고 여기선 제목을 검색할 것이다. i가 포함되면 중복을 필터링해준다는 뜻
            Q(content__icontains=kw) | # 내용 검색, 각각에 대한 중복처리
            Q(author__username__icontains=kw) | # 질문 글쓴이
            Q(answer__author__username__icontains=kw) # 답변 글쓴이
        ).distinct() #distinct는 중복을 처리해줌.

    # 페이징 처리 - 공식처럼 다른 곳에서도 이렇게 똑같은 코드가 쓰인다.
    paginator = Paginator(question_list, 10)  # 페이지에서 글을 10개씩 잘라서 보이게 하겠다.
    page_obj = paginator.get_page(page)

    # Question_list 이렇게 받아서 넘겨주겠다. 이 객체 안에 질문들이 다 들어가있다.

    context = {'question_list': page_obj, 'page' : page, 'kw': kw, 'so': so}  # 앞에 있는게 key, 뒤에있는데 value이다. dictionary 객체 내부에 키밸류 형태로 저장이 되어 있다.
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