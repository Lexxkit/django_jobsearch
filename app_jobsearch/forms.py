from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from app_jobsearch.models import Specialty, Resume


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=25, label='Имя',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, label='Фамилия',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')


class ApplicationForm(forms.Form):
    written_username = forms.CharField(max_length=128, label='Вас зовут',
                                       widget=forms.TextInput(attrs={'class': 'form-control'}))
    written_phone = forms.CharField(max_length=32, label='Ваш телефон',
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    written_cover_letter = forms.CharField(label='Сопроводительное письмо',
                                           widget=forms.Textarea(attrs={'class': 'form-control'}))


class CompanyForm(forms.Form):
    name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    logo = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    employee_count = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))


class VacancyForm(forms.Form):
    title = forms.CharField(max_length=128,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all(),
                                       widget=forms.Select(attrs={'class': 'custom-select mr-sm-2'}))
    skills = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                          'rows': '3',
                                                          'style': 'color:#000;'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                               'rows': '13',
                                                               'style': 'color:#000;'}))
    salary_min = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    salary_max = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ['user']
        widgets = {
            'education_name': forms.Textarea(attrs={'rows': 3}),
            'experience': forms.Textarea(attrs={'rows': 3})
        }
