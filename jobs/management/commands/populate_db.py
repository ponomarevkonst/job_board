import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from job_board.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR
from jobs.models import Specialty, Company, Vacancy
from django.utils import timezone

jobs = [

    {"title": "Разработчик на Python", "cat": "backend", "company": "staffingsmarter", "salary_from": "100000",
     "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Разработчик в проект на Django", "cat": "backend", "company": "swiftattack", "salary_from": "80000",
     "salary_to": "90000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Разработчик на Swift в аутсорс компанию", "cat": "backend", "company": "swiftattack",
     "salary_from": "120000", "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Мидл программист на Python", "cat": "backend", "company": "workiro", "salary_from": "80000",
     "salary_to": "90000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Питонист в стартап", "cat": "backend", "company": "primalassault", "salary_from": "120000",
     "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"}

]

""" Компании """

companies = [

    {"title": "workiro"},
    {"title": "rebelrage"},
    {"title": "staffingsmarter"},
    {"title": "evilthreath"},
    {"title": "hirey"},
    {"title": "swiftattack"},
    {"title": "troller"},
    {"title": "primalassault"}

]

""" Категории """

specialties = [

    {"code": "frontend", "title": "Фронтенд"},
    {"code": "backend", "title": "Бэкенд"},
    {"code": "gamedev", "title": "Геймдев"},
    {"code": "devops", "title": "Девопс"},
    {"code": "design", "title": "Дизайн"},
    {"code": "products", "title": "Продукты"},
    {"code": "management", "title": "Менеджмент"},
    {"code": "testing", "title": "Тестирование"}

]


class Command(BaseCommand):
    help = 'Command for filling database with prepared data'

    def handle(self, *args, **options):
        User.objects.create_user('user', 'user@example.com', 'userpass')
        user=User.objects.first()
        for specialty in specialties:
            picture_name = '/specty_' + specialty['code'] + '.png'
            picture_path = MEDIA_SPECIALITY_IMAGE_DIR + picture_name
            Specialty(code=specialty['code'], title=specialty['title'], picture=picture_path).save()

        for company in companies:
            logo_name = company['title'] + '.png'
            logo_path = MEDIA_COMPANY_IMAGE_DIR + '/' + logo_name
            Company(name=company['title'], user_id=user.id, employee_count=random.randint(10, 50), logo=logo_path).save()

        for job in jobs:
            specialty = Specialty.objects.filter(code=job['cat'])[0]
            company = Company.objects.filter(name=job['company'])[0]
            Vacancy(title=job['title'], specialty=specialty, company=company,
                    description=job['desc'], published_at=timezone.now(),
                    salary_min=int(job['salary_from']), salary_max=int(job['salary_to'])).save()
