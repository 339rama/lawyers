from django.forms import ModelForm
from mainapp.models import Question


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['email', 'phone_number', 'question']
