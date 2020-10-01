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

from jobs.views import vacancies_view, companies_view, index_view, custom_handler404, custom_handler500, MyLoginView, \
    MySignupView, application

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('companies/<int:company_id>', companies_view, name='company'),
    path('vacancies/<str:id>', vacancies_view, name='vacancy'),
    path('vacancies/cat/<str:id>', vacancies_view, name='vacancies_by_category'),
    path('vacancies/', vacancies_view, name='vacancies'),
    path('vacancies/<vacancy_id>/send', application, name='application'),
    # path('mycompany/', vacancies_view, name='mycompany'),
    # path('mycompany/vacancies', vacancies_view, name='vacancies_of_mycompany'),
    # path('mycompany/vacancies/<vacancy_id>', vacancies_view, name='my_vacancy'),
    path('login', MyLoginView.as_view(), name='login'),
    path('register', MySignupView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = custom_handler404
handler500 = custom_handler500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
