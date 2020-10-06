from django.contrib import admin
from .models import Company, Vacancy, Specialty, Application
from account.models import Resume

admin.site.register(Company)
admin.site.register(Vacancy)
admin.site.register(Specialty)
admin.site.register(Application)
admin.site.register(Resume)

# Register your models here.
