import copy

from django.shortcuts import render

# Create your views here.

QUESTIONS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'Text for question {i}',
        'img': "/img/img.jpg"
    } for i in range(30)
]
def index(request):
    return render(request, "index.html", context={'questions': QUESTIONS})

def hot(request):
    q = reversed(copy.deepcopy(QUESTIONS))
    return render(request, "hot.html", context={'questions': q})

def question(request, question_id):
    return render(request, "single_question.html", context={'question': QUESTIONS[question_id]})
