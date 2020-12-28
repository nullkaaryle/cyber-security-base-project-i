from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Choice, Question
from django.contrib.auth.models import User
from django.db.models.expressions import RawSQL
from django.db import connection

# Create your views here.


@login_required
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


@login_required
def detail(request, question_id):
    userLoggedIn = User.objects.get(username=request.user.username)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question, 'user': userLoggedIn})


@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def admin(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    user_list = User.objects.all
    context = {'latest_question_list': latest_question_list,
               'user_list': user_list}
    return render(request, 'polls/admin.html', context)

def search(request):
    if request.method == 'GET':
        context = {'search_term': ''}
        return render(request, 'polls/search.html', context)

    elif request.method == 'POST':
        
        question_searched = request.POST.get("search_term", "")
        cursor = connection.cursor()
        response = cursor.execute("SELECT * FROM polls_question WHERE question_text LIKE '%%%s%%'" % (question_searched)).fetchall()
        searched_questions = []
        for question in response:
            searched_questions.append(question[1])
        
        context = {'search_term': question_searched, 'db_result': searched_questions}
        return render(request, 'polls/search.html', context)
