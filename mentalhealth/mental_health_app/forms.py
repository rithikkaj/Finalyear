from django import forms
from .models import Assessment


class AssessmentForm(forms.ModelForm):
    """
    Form for Mental Health Assessment
    Collects responses and calculates scores for stress, anxiety, and depression
    """
    
    class Meta:
        model = Assessment
        fields = ['responses', 'stress_score', 'anxiety_score', 'depression_score', 
                  'work_hours', 'sleep_hours', 'prediction']
        widgets = {
            'responses': forms.HiddenInput(),
            'stress_score': forms.HiddenInput(),
            'anxiety_score': forms.HiddenInput(),
            'depression_score': forms.HiddenInput(),
            'work_hours': forms.NumberInput(attrs={'min': 0, 'max': 24}),
            'sleep_hours': forms.NumberInput(attrs={'min': 0, 'max': 24}),
            'prediction': forms.HiddenInput(),
        }

