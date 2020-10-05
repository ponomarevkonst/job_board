from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, CreateView
from django.views.generic.edit import DeleteView

from account.forms import ResumeForm, CompanyForm, VacancyForm
from account.models import Resume
from jobs.models import Company, Vacancy, Application


@method_decorator(login_required, name='dispatch')
class MyUpdateView(UpdateView):
    def get_object(self, **kwargs):
        return self.model.objects.filter(user=self.request.user).first()

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))


@login_required
def myresume_dispatch(request):
    if request.user.resumes.first():
        return HttpResponseRedirect(reverse('myresume_edit'))
    return render(request, 'resume/resume-create.html')


class ResumeEditView(MyUpdateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'resume/resume-edit.html'


@method_decorator(login_required, name='dispatch')
class ResumeCreateView(CreateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'resume/resume-edit.html'


@login_required
def mycompany_dispatch(request):
    if request.user.company_set.first():
        return HttpResponseRedirect(reverse('mycompany_edit'))
    return render(request, 'company/company-create.html')


class CompanyEditView(MyUpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/company-edit.html'


@method_decorator(login_required, name='dispatch')
class CompanyCreateView(CreateView):
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
class VacancyCreateView(CreateView):
    model = Vacancy
    template_name = 'vacancy/vacancy-create.html'
    form_class = VacancyForm

    def form_valid(self, form):
        vacancy = form.save(commit=False)
        vacancy.company = self.request.user.company_set.first()
        vacancy.save()
        return HttpResponseRedirect(reverse_lazy('mycompany_vacancy_edit', args=(vacancy.id,)))


@method_decorator(login_required, name='dispatch')
class VacancyDeleteView(DeleteView):
    model = Vacancy
    success_url = reverse_lazy('mycompany_vacancy_list')


@method_decorator(login_required, name='dispatch')
class VacancyEditView(UpdateView):
    model = Vacancy
    template_name = 'vacancy/vacancy-edit.html'
    form_class = VacancyForm

    def get(self, request, *args, **kwargs):
        company = Company.objects.filter(vacancies__id=self.kwargs['pk']).first()
        if company.is_owner(request.user):
            return super(VacancyEditView, self).get(self, request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy('mycompany_vacancy_list'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = Application.objects.filter(vacancy_id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))
