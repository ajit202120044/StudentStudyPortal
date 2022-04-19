from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.core.exceptions import ValidationError



class DateInput(forms.DateInput):
    input_type = 'date'

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        widgets = {'due' : DateInput()}
        fields = ['subject','title','description','due', 'marks','pdffile']  


   