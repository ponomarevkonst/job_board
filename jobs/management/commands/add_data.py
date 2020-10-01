from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from data import specialties, companies, jobs
from jobs.models import Specialty, Company, Vacancy


class Command(BaseCommand):
    help = 'Command for filling database with prepared data'

    def handle(self, *args, **options):
        user = User.objects.first()
        for specialty in specialties:
            Specialty(code=specialty['code'], title=specialty['title']).save()

        for company in companies:
            Company(name=company['title'], employee_count=100, owner=user).save()

        for job in jobs:
            specialty = Specialty.objects.filter(code=job['cat'])[0]
            company = Company.objects.filter(name=job['company'])[0]
            Vacancy(title=job['title'], specialty=specialty, company=company,
                    description=job['desc'], published_at=job['posted'],
                    salary_min=int(job['salary_from']), salary_max=int(job['salary_to'])).save()
