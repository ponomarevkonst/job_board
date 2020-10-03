from django import forms
from django.core.validators import RegexValidator

from account.models import Resume


class ResumeForm(forms.ModelForm):
    userName = forms.CharField(label='Имя', min_length=2)
    surname = forms.CharField(label='Фамилия', min_length=2)
    phone = forms.CharField(label='Номер телефона', min_length=11,
                            validators=[RegexValidator(regex=r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$",
                                                       message='Неверно введен номер телефона')])
    status = forms.CharField(label='Имя', min_length=2)
    salary = forms.IntegerField(label='Ожидаемое вознаграждение')
    class Meta:
        model = Resume
        fields = ('name', 'surname', 'phone', 'status', 'salary', 'specialty', 'grade', 'education', 'experience', 'portfolio')


