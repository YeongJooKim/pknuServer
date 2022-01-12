from django.urls import path
from django.contrib.auth import views as auth_views #계정과 관련된 library를 가져와서 로그인을 함.
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name = 'common/login.html'), name='login'), #request에 로그인을 클릭하면 common의 login으로 링크가 걸고
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
] #원래 규정된 길이 있는데(파일을 하나 만들어서 거기에 넣기) 그 방식대로 안함.