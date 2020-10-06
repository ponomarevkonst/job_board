import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from data import specialties, companies, jobs
from job_board.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR
from jobs.models import Specialty, Company, Vacancy
from django.utils import timezone


class Command(BaseCommand):
    help = 'Command for filling database with prepared data'

    def handle(self, *args, **options):
        user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass', last_login=timezone.now())
        user_id = user.id
        for specialty in specialties:
            picture_name = '/specty_' + specialty['code'] + '.png'
            picture_path = MEDIA_SPECIALITY_IMAGE_DIR + picture_name
            Specialty(code=specialty['code'], title=specialty['title'], picture=picture_path).save()

        for company in companies:
            logo_name = company['title'] + '.png'
            logo_path = MEDIA_COMPANY_IMAGE_DIR + '/' + logo_name
            Company(name=company['title'], employee_count=random.randint(10, 50), user_id=user_id, logo=logo_path).save()

        for job in jobs:
            specialty = Specialty.objects.filter(code=job['cat'])[0]
            company = Company.objects.filter(name=job['company'])[0]
            Vacancy(title=job['title'], specialty=specialty, company=company,
                    description=job['desc'], published_at=timezone.now(),
                    salary_min=int(job['salary_from']), salary_max=int(job['salary_to'])).save()
