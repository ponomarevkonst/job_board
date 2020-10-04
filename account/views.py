from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from account.forms import ResumeForm, CompanyForm
from account.models import Resume
from jobs.models import Company


@method_decorator(login_required, name='dispatch')
class MyCreateEditView(View):
    Model = None
    Form = None
    template_create = None
    template_edit = None
    update = False

    def get(self, request, **kwargs):
        instance = self.Model.objects.filter(user=request.user).first()
        form = self.Form(instance=instance if instance else None)
        context = {'form': form, 'update': self.update}
        if instance or kwargs['action']:
            return render(request, self.template_edit, context)
        return render(request, self.template_create, context)

    def post(self, request, **kwargs):
        instance = self.Model.objects.filter(user=request.user).first()
        form = self.Form(request.POST, request.FILES)
        context = {'form': form, 'update': self.update}
        if form.is_valid():
            if instance:
                instance.delete()
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            self.update = True
        return render(request, self.template_edit, context)


class MyResumeView(MyCreateEditView):
    Model = Resume
    Form = ResumeForm
    template_create = 'resume-create.html'
    template_edit = 'resume-edit.html'

class MyCompanyView(MyCreateEditView):
    Model = Company
    Form = CompanyForm
    template_create = 'company-create.html'
    template_edit = 'company-edit.html'


@login_required
def resumes_view(request, action, update=False):
    resume = Resume.objects.filter(user=request.user).first()
    form = ResumeForm(request.POST or (resume.__dict__ if resume else None))
    if request.method == 'GET':
        if resume or action:
            return render(request, 'resume/resume-edit.html', {'form': form, 'update': update})
        return render(request, 'resume/resume-create.html')
    if request.method == 'POST' and form.is_valid():
        if resume:
            resume.delete()
        resume = form.save(commit=False)
        resume.user = request.user
        resume.save()
        update = True
    return render(request, 'resume/resume-edit.html', {'form': form, 'update': update})


@login_required
def mycompany_view(request, action, update=False):
    company = Company.objects.filter(owner=request.user).first()
    if request.method == 'GET':
        form = CompanyForm(company.__dict__ if company else None)
        if company or action:
            return render(request, 'company/company-edit.html', {'form': form, 'update': update})
        return render(request, 'company/company-create.html')
    form = CompanyForm(request.POST, request.FILES)
    if request.method == 'POST' and form.is_valid():
        if company:
            company.delete()
        company = form.save(commit=False)
        company.user = request.user
        company.save()
        update = True
    return render(request, 'company/company-edit.html', {'form': form, 'update': update})
