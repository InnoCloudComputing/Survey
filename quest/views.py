from django.http import HttpResponseRedirect
from django.shortcuts import render

from forms import ResponseForm
from models import Question, Survey, Category
from quest.models import *


def index(request):
    return render(request, 'index.html')


def survey_detail(request):
    survey = Survey.objects.get(id=1)
    category_items = Category.objects.filter(survey=survey)
    categories = [c.name for c in category_items]
    if request.method == 'POST':
        form = ResponseForm(request.POST, survey=survey)
        if form.is_valid():
            response = form.save()
            return HttpResponseRedirect("/confirm/%s" % response.interview_uuid)
    else:
        form = ResponseForm(survey=survey)
    # TODO sort by category
    return render(request, 'survey.html', {'response_form': form, 'survey': survey, 'categories': categories})


def confirm(request, uuid):
    email = 'support@email.com'
    return render(request, 'confirm.html', {'uuid': uuid, "email": email})


def privacy(request):
    return render(request, 'privacy.html')

def survey_statistic(request):
    # get all questions
    questions = Question.objects.all()
    result = "{"
    for q in questions:
        # get all answers for the question
        question_variants = [x.strip() for x in q.choices.split(",")]
        if q.question_type == Question.RADIO:
            result += "\"" + q.text + "\":["
            for v in question_variants:
                count = AnswerRadio.objects.filter(body=v).count()
                result += "{\"" + v + "\":" + str(count) + "},"
            result = result[:-1] + "],"
        elif q.question_type == Question.SELECT:
            result += "\"" + q.text + "\":["
            for v in question_variants:
                count = AnswerSelect.objects.filter(body=v).count()
                result += "{\"" + v + "\":" + str(count) + "},"
            result = result[:-1] + "],"
        elif q.question_type == Question.SELECT_MULTIPLE:
            result += "\"" + q.text + "\":["
            for v in question_variants:
                count = AnswerSelectMultiple.objects.filter(body=v).count()
                result += "{\"" + v + "\":" + str(count) + "},"
            result = result[:-1] + "],"
        elif q.question_type == Question.INTEGER:
            result += "\"" + q.text + "\":["
            answers = AnswerInteger.objects.filter(question=q)
            sum = 0
            for a in answers:
                sum += a.body
            sum /= answers.count()
            result += "{\"Average\":" + str(sum) + "},"
            result = result[:-1] + "],"
    result = result[:-1] + "}"
    print result
    return render(request, 'statistics.html', {'results': result})

