from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, TemplateView, DetailView, ListView
from django.views import View
from django.shortcuts import redirect

from accounts.mixins import CompanyAccessMixin
from accounts.forms import CompanyForm, VacancyForm
from hiring.models import Company, Vacancy, Application


class MyLoginView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'


class MySignupView(CreateView):
    form_class = UserCreationForm
    success_url = '/login'
    template_name = 'accounts/register.html'


class SentView(TemplateView):
    template_name = 'accounts/sent.html'


class LetsStartCompanyView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/company-create.html'


class CreateCompanyView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    template_name = 'accounts/company-edit.html'
    success_message = 'Информация о компании обновлена'
    form_class = CompanyForm

    def get_context_data(self, **kwargs):
        form = CompanyForm
        context = super(CreateCompanyView, self).get_context_data(**kwargs)
        context['company'] = Company.objects.filter(owner_id=self.request.user.id)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            create_company = form.save(commit=False)
            form.instance.owner_id = request.user.id
            create_company.save()
            return redirect('my_company')
        return render(request, 'accounts/company-edit.html', context={'form': form})



class MyCompanyView(LoginRequiredMixin, CompanyAccessMixin, TemplateView):
    template_name = 'accounts/company-edit.html'

    def get_context_data(self, **kwargs):
        company = Company.objects.get(owner_id=self.request.user.id)
        form_context = {
            'name': company.name,
            'employee_count': company.employee_count,
            'location': company.location,
            'description': company.description,
            'logo': company.logo.url,
        }
        form = CompanyForm(form_context)
        context = super(MyCompanyView, self).get_context_data(**kwargs)
        context['company_edit'] = company
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CompanyForm(request.POST)
        if form.is_valid():
            create_company = form.save(commit=False)
            form.instance.owner_id = request.user.id
            create_company.save()
        return render(request, 'accounts/company-edit.html', context={'form': form})


class CompanyVacanciesView(LoginRequiredMixin, CompanyAccessMixin, ListView):
    template_name = 'accounts/vacancy-list.html'
    model = Vacancy
    context_object_name = 'vacancies'

    def get_queryset(self):
        self.vacancy = Vacancy.objects.filter(company_id__owner_id=self.request.user.id) \
            .annotate(applications_count=Count('applications'))
        return self.vacancy


class CreateVacancyView(LoginRequiredMixin, CompanyAccessMixin, TemplateView):
    template_name = 'accounts/vacancy-edit.html'

    def get_context_data(self, **kwargs):
        form = VacancyForm
        context = super(CreateVacancyView, self).get_context_data(**kwargs)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = VacancyForm(request.POST)
        if form.is_valid():
            create_vacancy = form.save(commit=False)
            form.instance.published_as = '%Y-%m-%d'
            create_vacancy.save()
            return redirect('my_company_vacancies')
        return render(request, 'accounts/company-edit.html', context={'form': form})


class MyCompanyVacansyView(TemplateView):
    template_name = 'accounts/vacancy-edit.html'
    pk_url_kwarg = 'vacancy_id'

    def get_context_data(self, **kwargs):
        vacancy = Vacancy.objects.get(id=self.kwargs['vacancy_id'])
        form_context = {
            'title': vacancy.title,
            'specialty': vacancy.specialty,
            'skills': vacancy.skills,
            'description': vacancy.description,
            'salary_min': vacancy.salary_min,
            'salary_max': vacancy.salary_max,
        }
        form = VacancyForm(form_context)
        context = super(MyCompanyVacansyView, self).get_context_data(**kwargs)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = VacancyForm(request.POST)
        if form.is_valid():
            create_vacancy = form.save(commit=False)
            form.instance.published_as = '%Y-%m-%d'
            create_vacancy.save()
            return redirect('my_company_vacancy')
        return render(request, 'accounts/company-edit.html', context={'form': form})

# Create your views here.
