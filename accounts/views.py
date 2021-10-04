from datetime import date

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import UpdateView
from hiring.models import Company, Vacancy

from accounts.forms import CompanyForm, VacancyForm
from accounts.mixins import CompanyAccessMixin, MyCompanyVacanciesMixin


class MyLoginView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'


class MySignupView(CreateView):
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_url = '/login'


class SentView(TemplateView):
    template_name = 'accounts/sent.html'


class LetsStartMyCompanyView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/company-create.html'


class MyCompanyBaseView(LoginRequiredMixin, SuccessMessageMixin):
    template_name = 'accounts/company-edit.html'
    model = Company
    form_class = CompanyForm
    success_url = reverse_lazy('my_company')


class CreateMyCompanyView(MyCompanyBaseView, CreateView):
    success_message = 'Компания создана'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MyCompanyView(MyCompanyBaseView, CompanyAccessMixin, UpdateView):
    success_message = 'Информация о компании обновлена'
    context_object_name = 'company_edit'

    def get_object(self):
        return self.request.user.company


class MyCompanyVacanciesView(LoginRequiredMixin, CompanyAccessMixin, ListView):
    template_name = 'accounts/vacancy-list.html'
    model = Vacancy
    context_object_name = 'vacancies'

    def get_queryset(self):
        self.vacancy = Vacancy.objects.filter(company_id__owner_id=self.request.user.id) \
            .annotate(applications_count=Count('applications'))
        return self.vacancy


class MyCompanyVacancyBaseView(LoginRequiredMixin, CompanyAccessMixin, SuccessMessageMixin):
    template_name = 'accounts/vacancy-edit.html'
    model = Vacancy
    form_class = VacancyForm


class CreateVacancyView(MyCompanyVacancyBaseView, CreateView):
    success_message = 'Вакансия создана'
    success_url = reverse_lazy('my_company_vacancies')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.company = self.request.user.company
        form.instance.published_as = date.today()
        return super().form_valid(form)


class MyCompanyVacancyView(MyCompanyVacancyBaseView, MyCompanyVacanciesMixin, UpdateView):
    success_message = 'Информация о вакансии обновлена'
    pk_url_kwarg = 'vacancy_id'

    def get_success_url(self) -> str:
        success_url = reverse_lazy('my_company_vacancy', args=(self.kwargs['vacancy_id'],))
        return success_url


# Create your views here.
