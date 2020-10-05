from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, FormView, UpdateView, CreateView

from account.forms import ResumeForm, CompanyForm, VacancyForm
from account.models import Resume
from jobs.models import Company, Vacancy


# def is_owner(f): TODO make it work
#     @wraps(f)
#     def wrap(self, request, *args, **kwargs):
#         if not request.user.company_set.filter(id=kwargs['id']):
#             return HttpResponseForbidden()
#         bound_method = f.__get__(self, type(self))
#         return bound_method(self, *args, **kwargs)
#     return wrap


class MyUpdateView(UpdateView):
    def get_object(self, **kwargs):
        return self.model.objects.filter(user=self.request.user).first()


class MyCreateView(CreateView):
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)


def myresume_dispatch(request):
    if request.user.resumes.first():
        return HttpResponseRedirect(reverse('myresume_edit'))
    return HttpResponseRedirect(reverse('myresume_create'))


class ResumeEditView(MyUpdateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'resume/resume-edit.html'


class ResumeCreateView(MyCreateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'resume/resume-edit.html'


def mycompany_dispatch(request):
    if request.user.company_set.first():
        return HttpResponseRedirect(reverse('mycompany_edit'))
    return HttpResponseRedirect(reverse('mycompany_create'))


class CompanyEditView(MyUpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/company-edit.html'


class CompanyCreateView(MyCreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/company-edit.html'





@method_decorator(login_required, name='dispatch')
class VacancyListView(ListView):
    template_name = 'vacancy/vacancy-list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        company = self.request.user.company_set.first()
        vacancies = company.vacancies.all()
        return vacancies


@method_decorator(login_required, name='dispatch')
class VacancyEditView(UpdateView):
    model = Vacancy
    template_name = 'vacancy/vacancy-edit.html'
    form_class = VacancyForm

    def get_object(self, queryset=None):
        id = self.kwargs['pk']
        if self.request.user.company_set.filter(id=id):
            return Vacancy.objects.filter(id=id).first()

    # def get(self, request, *args, **kwargs):
    #     id = kwargs['id']
    #     if request.user.company_set.filter(id=id):
    #         vacancy = Vacancy.objects.filter(id=id).first()
    #         form = VacancyForm(instance=vacancy)
    #         return render(request, 'vacancy/vacancy-edit.html', {'form': form, 'vacancy': vacancy})
    #     return HttpResponseForbidden()
    #
    # def post(self, request, *args, **kwargs):
    #     id = kwargs['id']
    #     form = VacancyForm(request.POST)
    #     if form.is_valid():
    #         form.save()
