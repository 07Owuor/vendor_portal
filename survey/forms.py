from django import forms
from .models import Survey


class SurveyForm(forms.ModelForm):
    MOOD = [
        ('Happy', 'Happy'),
        ('Okay', 'Okay'),
        ('Concerned', 'Concerned'),
        ('Sad', 'Sad')
    ]
    LOCATION = [
        ('KNE', 'KNE'),
        ('KLF', 'KLF'),
        ('Farm Star', 'Farm Star'),
        ('Sameer', 'Sameer')
    ]
    location = forms.ChoiceField(
        choices=LOCATION
    )
    mood = forms.ChoiceField(
        choices=MOOD,
        label="How was your satisfaction level this week?",
        widget=forms.RadioSelect(
            attrs={
                'class': 'form-control',
                'type': 'radio'
            }
        )
    )


    mood_explanation = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Please let us know any specific positive feedback or concern you might have'
    }))

    class Meta:
        model = Survey
        exclude = ('created_at',)


class DateInput(forms.DateInput):
    input_type = 'date'
    format = ["%Y-%m-%d"]


class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)