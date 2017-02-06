from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.contrib import messages
import datetime
from quest.models import AnswerBase, AnswerInteger, AnswerRadio, AnswerSelect, AnswerSelectMultiple

from models import Question, Survey, Category
from forms import ResponseForm


def index(request):
    return render(request, 'index.html')


def survey_detail(request):
    survey = Survey.objects.get(id=1)
    category_items = Category.objects.filter(survey=survey)
    categories = [c.name for c in category_items]
    print 'categories for this survey:'
    print categories
    if request.method == 'POST':
        form = ResponseForm(request.POST, survey=survey)
        if form.is_valid():
            response = form.save()
            return HttpResponseRedirect("/confirm/%s" % response.interview_uuid)
    else:
        form = ResponseForm(survey=survey)
        print form
    # TODO sort by category
    return render(request, 'survey.html', {'response_form': form, 'survey': survey, 'categories': categories})


def confirm(request, uuid):
    email = 'support@email.com'
    return render(request, 'confirm.html', {'uuid': uuid, "email": email})


def privacy(request):
    return render(request, 'privacy.html')

def calc_radio(q, answers):
    q.get_choices


def calc_select(q, answers):
    return []


def calc_select_mult(q, answers):
    return []


def calc_integer(q, answers):
    return []


def survey_statistic(request):
    # get all questions
    questions = Question.objects.all()
    result = None
    results = []
    for q in questions:
        # get all answers for the question
        answers = AnswerBase.objects.filter(question=q)
        if len(answers) > 0:
            if answers[0] is AnswerRadio:
                result = calc_radio(q, answers)
                results.append(("Radio", q.get_choices()))
            elif answers[0] is AnswerSelect:
                result = calc_select(q, answers)
            elif answers[0] is AnswerSelectMultiple:
                result = calc_select_mult(q, answers)
            elif answers[0] is AnswerInteger:
                result = calc_integer(q, answers)
            results.append((q, result))
    return render(request, 'statistics.html', {'results': results})
