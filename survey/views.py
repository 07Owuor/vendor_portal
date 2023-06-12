from django.shortcuts import render, redirect, HttpResponse
from datetime import date, timedelta, datetime as dt
from .forms import SurveyForm, DateRangeForm
from django.contrib import messages
from .models import Survey
from io import StringIO
import csv

# Create your views here.


def survey_home(request):
    template_name = 'survey/survey.html'
    if request.method == 'POST':
        form = SurveyForm(request.POST or None)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.save()
            messages.success(request, "Thank you for your honest feedback")
            return redirect('survey_home')
    else:
        form = SurveyForm()

    data = {
        'form': form
    }
    return render(request, template_name, data)


def survey_dash(request):
    template_name = 'survey/survey_dash.html'
    surveys = Survey.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = DateRangeForm(request.POST or None)
        if form.is_valid():
            d_start = str(str(form.cleaned_data['start_date']) + " " + str(dt.now().time()))
            d_end = str(str(form.cleaned_data['end_date']) + " " + str(dt.now().time()))
            start_date = dt.strptime(d_start, "%Y-%m-%d %H:%M:%S.%f")
            end_date = dt.strptime(d_end, "%Y-%m-%d %H:%M:%S.%f")
            print(end_date, start_date)

            survey_data = Survey.objects.filter(
                created_at__range=(start_date, end_date)
            )
            f = StringIO()
            writer = csv.writer(f)
            writer.writerow(['Name', 'Email', 'Phone Number', 'Location', 'Mood', 'Explanation', 'Created At'])
            for s in survey_data:

                phone_number = "'"+str(s.phone_number)+"'"
                writer.writerow(
                    [s.name, s.email, str(phone_number), s.location, s.mood, s.mood_explanation, s.created_at.date()])

            f.seek(0)
            response = HttpResponse(f, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=Surveys.csv'
            return response

    else:
        form = DateRangeForm()

    data = {
        'surveys': surveys,
        'form': form
    }

    return render(request, template_name, data)