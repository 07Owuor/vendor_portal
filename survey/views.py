from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SurveyForm
from .models import Survey

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
    data = {
        'surveys': surveys,
    }

    return render(request, template_name, data)