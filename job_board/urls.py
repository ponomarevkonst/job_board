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
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from account.views import resumes_view, mycompany_view, MyResumeView, MyCompanyView
from jobs.views import vacancies_view, index_view, custom_handler404, custom_handler500, MyLoginView, \
    MySignupView, application, companies_view, search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('companies/<int:company_id>', companies_view, name='company'),
    path('vacancies/<str:id>', vacancies_view, name='vacancy'),
    path('vacancies/cat/<str:id>', vacancies_view, name='vacancies_by_category'),
    path('vacancies/', vacancies_view, name='vacancies'),
    path('vacancies/<vacancy_id>/send', application, name='application'),

    re_path('myresume/(?P<action>edit|create|.*)$', MyResumeView.as_view(), name='myresume'),
    re_path('mycompany/(?P<action>edit|create|.*)$', MyCompanyView.as_view(), name='mycompany'),

    path('search/', search, name='search'),
    path('search/<query>', search, name='search_with_param'),
    path('login', MyLoginView.as_view(), name='login'),
    path('register', MySignupView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = custom_handler404
handler500 = custom_handler500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
