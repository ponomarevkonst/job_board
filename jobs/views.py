from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect, request as req
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView
from job_board.settings import LOGIN_REDIRECT_URL
from jobs.forms import RegisterForm, ApplicationForm, SearchForm
from jobs.models import Company, Vacancy, Specialty


class MySignupView(CreateView):
    form_class = RegisterForm
    success_url = 'login'
    template_name = 'register.html'

    def form_valid(self, form):
        form.save()
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(self.request, user)
        return HttpResponseRedirect(LOGIN_REDIRECT_URL)


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


def index_view(request):
    context = {'specialties': [], 'companies': [], 'form': SearchForm(),
               'examples': ['Python', 'Flask', 'Django', 'Парсинг', 'ML']}
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
            category_name = Specialty.objects.filter(code=id).first().title
            context['category_name'] = category_name if category_name else 'Категория не найдена'
            context['vacancies'] = Vacancy.objects.filter(specialty__code=id).all()
    else:  # get all vacancies
        context['category_name'] = 'Все вакансии'
        context['vacancies'] = Vacancy.objects.all()
    return render(request, 'vacancies.html', context)


def application(request, vacancy_id):
    form = ApplicationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        application = form.save(commit=False)
        application.vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        application.user = request.user
        application.save()
        return render(request, 'sent.html', {"vacancy_id": vacancy_id})


@csrf_exempt
def search(request, query=None):
    if not query:
        query = request.GET['query']
    form = SearchForm({'query': query})
    context = {'results': [], 'form': form}
    if form.is_valid():
        query = form.cleaned_data['query']
        context['vacancies'] = Vacancy.objects.annotate(search=SearchVector('title', 'description')).filter(search=query)
    return render(request, 'search_page.html', context)



def custom_handler404(request, exception):
    return HttpResponseNotFound('404')


def custom_handler500(request, *args):
    return HttpResponseServerError('500')
