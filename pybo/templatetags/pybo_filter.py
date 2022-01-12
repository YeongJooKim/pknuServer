import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def mark(value):
    extensions = ["nl2br", "fenced_code"] #markdown 소스코드를 사용하기 위해 fenced_code 이 코드를 가져옴
    return mark_safe(markdown.markdown(value, extensions=extensions)) #얘는 제공되는 함수이다. extensions은 속성이다. 위에꺼랑 다른거고 mark_safe얘는 html로 만들어줌(?)
