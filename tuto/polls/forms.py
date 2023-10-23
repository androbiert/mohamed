# forms.py
from django import forms
from .models import Choice  # Adjust the import based on your project structure
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        
class ChoiceSuggestionForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
