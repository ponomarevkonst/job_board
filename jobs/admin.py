from django.contrib import admin
from jobs.models import Company, Vacancy, Specialty, Application

admin.site.register(Company)
admin.site.register(Vacancy)
admin.site.register(Specialty)
admin.site.register(Application)

# Register your models here.
