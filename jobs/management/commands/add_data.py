import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from data import specialties, companies, jobs
from jobs.models import Specialty, Company, Vacancy


class Command(BaseCommand):
    help = 'Command for filling database with prepared data'

    def handle(self, *args, **options):
        user = User.objects.first()
        for specialty in specialties:
            picture_name = 'specty_' + specialty['code'] + '.png'
            picture_path = 'speciality_images/' + picture_name
            spec = Specialty(code=specialty['code'], title=specialty['title'], picture=picture_path).save()

        for company in companies:
            picture_name = company['title'] + '.png'
            logo_path = 'company_images/' + picture_name
            company = Company(name=company['title'], employee_count=random.randint(10, 50), owner=user, logo=logo_path).save()

        for job in jobs:
            specialty = Specialty.objects.filter(code=job['cat'])[0]
            company = Company.objects.filter(name=job['company'])[0]
            Vacancy(title=job['title'], specialty=specialty, company=company,
                    description=job['desc'], published_at=job['posted'],
                    salary_min=int(job['salary_from']), salary_max=int(job['salary_to'])).save()
