from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Application


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Электропочта")
    first_name = forms.CharField(label="Имя", min_length=2)
    last_name = forms.CharField(label="Фамилия", min_length=2)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name",)

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ApplicationForm(forms.ModelForm):
    written_username = forms.CharField(label='Имя')
    written_phone = forms.CharField(label='Номер телефона')
    written_cover_letter = forms.CharField(label='Сопроводительное письмо', widget=forms.Textarea, required=False)

    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control w-100",
                                                          'placeholder': "Найти работу или стажировку",
                                                          'aria-label': "Найти работу или стажировку"}))
