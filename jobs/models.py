from django.contrib.auth.models import User
from django.db import models
from job_board.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Specialty(models.Model):
    code = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR, height_field='height_field', width_field='width_field')
    height_field = models.PositiveIntegerField(default=0)
    width_field = models.PositiveIntegerField(default=0)

    def delete(self, *args, **kwargs):
        self.picture.storage.delete(self.picture.path)
        super(Specialty, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title


class Company(models.Model):
    name = models.CharField(max_length=40)
    location = models.CharField(max_length=50)
    description = models.CharField(max_length=60)
    employee_count = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, height_field='height_field', width_field='width_field')
    height_field = models.PositiveIntegerField(default=0)
    width_field = models.PositiveIntegerField(default=0)

    def delete(self, *args, **kwargs):
        self.logo.storage.delete(self.logo.path)
        super(Company, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    title = models.CharField(max_length=200)
    specialty = models.ForeignKey(Specialty, related_name="vacancies", on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name="vacancies", on_delete=models.CASCADE)
    skills = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateTimeField()

    def __str__(self):
        return str(self.id) + ': ' + self.title


class Application(models.Model):
    written_username = models.CharField(max_length=30)
    written_phone = models.CharField(max_length=30)
    written_cover_letter = models.CharField(max_length=350)
    vacancy = models.ForeignKey(Vacancy, related_name="applications", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="applications", on_delete=models.CASCADE)

    def __str__(self):
        return self.written_username


