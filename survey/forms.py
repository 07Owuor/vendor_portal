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

    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-user',
        'type': 'text',
        'placeholder': 'Email Address'
    }))
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-user',
        'type': 'text',
        'placeholder': 'Your Name'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-user',
        'type': 'text',
        'placeholder': 'Phone Number'
    }))
    mood_explanation = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Please let us know any specific positive feedback or concern you might have'
    }))

    class Meta:
        model = Survey
        exclude = ('created_at',)
