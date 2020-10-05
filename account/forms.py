from crispy_forms.helper import FormHelper
from django import forms
from django.core.validators import RegexValidator
from account.choices import GRADE_CHOICES, SPECIALITY_CHOICES, WORK_STATUS_CHOICES
from account.models import Resume
from jobs.models import Company, Vacancy, Specialty


class MyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False


class ResumeForm(MyForm):
    experience = forms.CharField(widget=forms.Textarea)
    education = forms.CharField(widget=forms.Textarea)
    grade = forms.ChoiceField(choices=GRADE_CHOICES)
    specialty = forms.ChoiceField(choices=SPECIALITY_CHOICES)
    status = forms.ChoiceField(choices=WORK_STATUS_CHOICES)
    phone = forms.CharField(label='Номер телефона', min_length=11,
                            validators=[RegexValidator(regex=r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$",
                                                       message='Неверно введен номер телефона')])

    class Meta:
        model = Resume
        fields = ('phone', 'status', 'salary', 'specialty',
                  'grade', 'education', 'experience', 'portfolio')


class CompanyForm(MyForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Company
        fields = ('name', 'location', 'description', 'employee_count', 'logo')


class VacancyForm(MyForm):
    skills = forms.CharField(widget=forms.Textarea)
    description = forms.CharField(widget=forms.Textarea)
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all())

    class Meta:
        model = Vacancy
        fields = ('title', 'specialty', 'salary_min', 'salary_max', 'skills', 'description')
