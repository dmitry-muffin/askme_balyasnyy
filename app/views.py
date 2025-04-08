
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from app.models import Question, Answer

# Create your views here.

QUESTIONS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'Text for question {i}',
        'img': "/img/img.jpg"
    } for i in range(30)
]

def paginate(objects, request, per_page=10):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)
    return paginator.get_page(page_number)

def index(request):
    questions = Question.objects.get_new()
    page = paginate(questions, request)

    return render(request, "index.html", context={'questions': page.object_list, "page_obj": page})

def hot(request):
    questions = Question.objects.get_hot()
    page = paginate(questions, request)
    return render(request, "hot.html", context={'page_obj': page})


def question(request, question_id):

    question = get_object_or_404(Question, id=question_id)

    answers = Answer.objects.filter(question=question).order_by('-is_correct', '-created_at')
    page = paginate(answers,request,  per_page=50)

    context = {
        'question': question,
        'page': page,
        'answers_count': answers.count(),
        'answers': answers,
    }
    return render(request, "single_question.html", context)

def tag(request, tag_req):
    questions = Question.objects.with_tag(tag_req)
    page = paginate(questions, request)

    context = {
        'tag': tag_req,
        'page': page,
        'questions': page.object_list,
        'page_obj': page,
    }
    return render(request, "tag.html", context)

def ask(request):
    return render(request, "ask.html")

def login(request):
    return render(request, "login.html")
def register(request):
    return render(request, "register.html")
def settings(request):
    return render(request, "settings.html")
