from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect, request as req
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import CreateView
from jobs.forms import RegisterForm, ApplicationForm
from jobs.models import Company, Vacancy, Specialty, Application


class MySignupView(CreateView):
    form_class = RegisterForm
    success_url = 'login'
    template_name = 'register.html'

    def form_valid(self, form):
        form.save()
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(self.request, user)
        return HttpResponseRedirect(form.cleaned_data['next'])


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'



def index_view(request):
    context = {'specialties': [], 'companies': []}
    for company in Company.objects.all():
        context['companies'].append({'logo': company.logo, 'id': company.id,
                                     'vacancies_count': company.vacancies.count()})
    for specialty in Specialty.objects.all():
        context['specialties'].append({'picture': specialty.picture, 'title': specialty.title,
                                       'vacancies_count': specialty.vacancies.count(), 'code': specialty.code})
    return render(request, 'index.html', context)


def companies_view(request, company_id, context={}):
    company = get_object_or_404(Company, id=company_id)
    context['vacancies'] = company.vacancies.all()
    context['company'] = {'name': company.name, 'logo': company.logo}
    return render(request, 'company.html', context)


def vacancies_view(request, id=None, context={}):  # @TODO make 3 different classes for increasing readability
    if id:
        if id.isnumeric():  # get single vacancy by id
            context['vacancy'] = get_object_or_404(Vacancy, id=id)
            context['company'] = context['vacancy'].company
            context['form'] = ApplicationForm()
            return render(request, 'vacancy.html', context)
        else:  # get vacancies by category_id
            context['category_name'] = get_object_or_404(Specialty, code=id).title
            context['vacancies'] = get_list_or_404(Vacancy, specialty__code=id)
    else:  # get all vacancies
        context['category_name'] = 'Все вакансии'
        context['vacancies'] = Vacancy.objects.all()
    return render(request, 'vacancies.html', context)


def application(request, vacancy_id):
    form = ApplicationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        Application(written_username=data['written_username'], written_phone=data['written_username'],
                    written_cover_letter=data['written_cover_letter'], vacancy=get_object_or_404(Vacancy, id=vacancy_id),
                    user=request.user).save()
        return render(request, 'sent.html', {"vacancy_id": vacancy_id})



def custom_handler404(request, exception):
    return HttpResponseNotFound('404')


def custom_handler500(request, *args):
    return HttpResponseServerError('500')
