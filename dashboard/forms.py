from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.core.exceptions import ValidationError
# from django.contrib.auth.models import AbstractUser



# class UploadFileForm(forms.Form):
#     file = forms.FileField()

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']


class DateInput(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due' : DateInput()}
        fields = ['subject','title','description','due','is_finished']      

#common class for search form in youtube and books and disc serach 

class DashboardForm(forms.Form):
    text = forms.CharField( max_length=100,label = "Enter your serach :" )


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)


class Email(forms.EmailField): 
    def clean(self, value):
        super(Email, self).clean(value)
        try:
            User.objects.get(email=value)
            raise forms.ValidationError("This email is already registered. Use the 'forgot password' link on the login page")
        except User.DoesNotExist:
            return value

class YourForm(UserCreationForm):

    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
       return self.cleaned_data


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    
    class Meta:
        model = User
        # email = YourForm()
        fields = ['username','first_name','last_name','email','password1','password2']
        
class ConversionForm(forms.Form):

    CHOICES =[('length','Length'),('mass','Mass')]
    measurement = forms.ChoiceField(choices=CHOICES,widget = forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    CHOICES = [('yard','Yard'),('foot','Foot')]
    input = forms.CharField(required=False, label = False ,widget = forms.TextInput(


        attrs = {'type':'number','placeholder':'Enter the Number'}
    ))
    measure1 = forms.CharField(
        label = '', widget = forms.Select(choices = CHOICES)
    ) 
    measure2 = forms.CharField(
        label = '', widget = forms.Select(choices = CHOICES)
    ) 




class ConversionMassForm(forms.Form):
    CHOICES = [('pound','Pound'),('kilogram','Kilogram')]
    input = forms.CharField(required=False, label = False ,widget = forms.TextInput(


        attrs = {'type':'number','placeholder':'Enter the Number'}
    ))
    measure1 = forms.CharField(
        label = '', widget = forms.Select(choices = CHOICES)
    ) 
    measure2 = forms.CharField(
        label = '', widget = forms.Select(choices = CHOICES)
    ) 
