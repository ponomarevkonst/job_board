"""job_board URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from account.views import VacancyListView, VacancyEditView, ResumeEditView, \
    ResumeCreateView, myresume_dispatch, mycompany_dispatch, CompanyCreateView, CompanyEditView, VacancyCreateView, \
    VacancyDeleteView
from jobs.views import custom_handler404, custom_handler500, MyLoginView, \
    MySignupView, CompaniesView, search, CompaniesListView, IndexView, VacanciesListView, VacancyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),

    path('companies/<int:pk>', CompaniesView.as_view(), name='company'),
    path('companies/list', CompaniesListView.as_view(), name='company_list'),

    path('vacancies/cat/<pk>', VacanciesListView.as_view(), name='vacancies'),
    path('vacancies/', VacanciesListView.as_view(), name='vacancies_list'),
    path('vacancies/<pk>', VacancyView.as_view(), name='vacancy'),

    path('myresume/', myresume_dispatch, name='myresume'),
    path('myresume/edit', ResumeEditView.as_view(), name='myresume_edit'),
    path('myresume/create', ResumeCreateView.as_view(), name='myresume_create'),

    path('mycompany/', mycompany_dispatch, name='mycompany'),
    path('mycompany/edit', CompanyEditView.as_view(), name='mycompany_edit'),
    path('mycompany/create', CompanyCreateView.as_view(), name='mycompany_create'),
    path('mycompany/vacancy/list', VacancyListView.as_view(), name='mycompany_vacancy_list'),
    path('mycompany/vacancy/create', VacancyCreateView.as_view(), name='mycompany_vacancy_create'),
    path('mycompany/vacancy/edit/<pk>', VacancyEditView.as_view(), name='mycompany_vacancy_edit'),
    path('mycompany/vacancy/delete/<pk>', VacancyDeleteView.as_view(), name='mycompany_vacancy_delete'),

    path('search/', search, name='search'),
    path('search/<query>', search, name='search_with_param'),
    path('login', MyLoginView.as_view(), name='login'),
    path('register', MySignupView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout')
]

handler404 = custom_handler404
handler500 = custom_handler500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
