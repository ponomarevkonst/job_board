from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView

from account.forms import ResumeForm, CompanyForm
from account.models import Resume
from jobs.models import Company


@login_required
class CompanyVacancyListView(ListView):
    pass




@login_required
def resumes_view(request, action, update=False):
    resume = Resume.objects.filter(user=request.user).first()
    form = ResumeForm(request.POST or (resume.__dict__ if resume else None))
    if request.method == 'GET':
        if resume or action:
            return render(request, 'resume-edit.html', {'form': form, 'update': update})
        return render(request, 'resume-create.html')
    if request.method == 'POST' and form.is_valid():
        if resume:
            resume.delete()
        resume = form.save(commit=False)
        resume.user = request.user
        resume.save()
        update = True
    return render(request, 'resume-edit.html', {'form': form, 'update': update})


@login_required
def mycompany_view(request, action, update=False):
    company = Company.objects.filter(owner=request.user).first()
    if request.method == 'GET':
        form = CompanyForm(company.__dict__ if company else None)
        if company or action:
            return render(request, 'company-edit.html', {'form': form, 'update': update})
        return render(request, 'company-create.html')
    form = CompanyForm(request.POST, request.FILES)
    if request.method == 'POST' and form.is_valid():
        if company:
            company.delete()
        company = form.save(commit=False)
        company.owner = request.user
        company.save()
        update = True
    return render(request, 'company-edit.html', {'form': form, 'update': update})
