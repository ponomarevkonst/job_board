from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, TemplateView
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DetailView
from job_board.settings import LOGIN_REDIRECT_URL
from .forms import RegisterForm, ApplicationForm, SearchForm
from .models import Company, Vacancy, Specialty

SEARCH_EXAMPLES = ['Python', 'Flask', 'Django', 'Парсинг', 'ML']


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


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'specialties': Specialty.objects.all(), 'companies': Company.objects.all(),
                        'form': SearchForm(), 'examples': SEARCH_EXAMPLES})
        return context


class CompaniesListView(ListView):
    model = Company
    context_object_name = 'companies'
    template_name = 'company/company_list.html'


class CompaniesView(DetailView):
    model = Company
    template_name = 'company/company.html'
    context_object_name = 'company'


class VacanciesListView(ListView):
    model = Vacancy
    template_name = 'vacancy/vacancies.html'
    context_object_name = 'vacancies'

    def get_queryset(self, **kwargs):
        if 'pk' not in self.kwargs:
            return self.model.objects.all()
        return self.model.objects.filter(specialty__code=self.kwargs['pk'])


class VacancyView(CreateView):
    model = Vacancy
    form_class = ApplicationForm
    template_name = 'vacancy/vacancy.html'

    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        context['vacancy'] = self.model.objects.filter(id=self.kwargs['pk']).first()
        return context

    def get_form(self, **kwargs):
        if not self.request.user.is_anonymous:
            resume = self.request.user.resumes.first()
            if resume:
                user = self.request.user
                name = user.first_name + ' ' + user.last_name
                phone = resume.phone
                form_data = {'written_username': name, 'written_phone': phone}
                return self.form_class(form_data)
        return super(VacancyView, self).get_form(**kwargs)

    def form_valid(self, form):
        application = form.save(commit=False)
        application.vacancy = self.model.objects.filter(id=self.kwargs['pk']).first()
        application.user = self.request.user
        application.save()
        return render(self.request, 'sent.html', {"vacancy_id": self.kwargs['pk']})


@csrf_exempt
def search(request, query=None):
    if not query and 'query' in request.GET:
        query = request.GET['query']
    form = SearchForm({'query': query})
    context = {'results': [], 'form': form}
    if form.is_valid():
        query = form.cleaned_data['query']
        context['vacancies'] = Vacancy.objects.filter(Q(title__contains=query) | Q(description__contains=query)).all()
    return render(request, 'search/search_page.html', context)


def custom_handler404(request, exception):
    return HttpResponseNotFound('404')


def custom_handler500(request, *args):
    return HttpResponseServerError('500')
