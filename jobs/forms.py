from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Reset, ButtonHolder
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.forms import ModelForm

from jobs.models import Application


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


class ApplicationForm(ModelForm):
    written_username = forms.CharField(label='Имя')
    written_phone = forms.CharField(label='Номер телефона')
    written_cover_letter = forms.CharField(label='Сопроводительное письмо', widget=forms.Textarea)

    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')
