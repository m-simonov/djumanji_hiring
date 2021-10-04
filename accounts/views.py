from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from hiring.models import Company, Vacancy

from accounts.forms import CompanyForm, VacancyForm
from accounts.mixins import CompanyAccessMixin


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


class CreateMyCompanyView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    template_name = 'accounts/company-edit.html'
    success_message = 'Информация о компании обновлена'
    form_class = CompanyForm

    def get_context_data(self, **kwargs):
        form = CompanyForm
        context = super(CreateMyCompanyView, self).get_context_data(**kwargs)
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


class MyCompanyView(LoginRequiredMixin, CompanyAccessMixin, SuccessMessageMixin, UpdateView):
    template_name = 'accounts/company-edit.html'
    model = Company
    form_class = CompanyForm
    success_url = reverse_lazy('my_company')
    success_message = 'Информация о компании обновлена'
    context_object_name = 'company_edit'

    def get_object(self):
        return self.request.user.company


# class MyCompanyView(LoginRequiredMixin, CompanyAccessMixin, SuccessMessageMixin, TemplateView):
#     template_name = 'accounts/company-edit.html'
#     success_message = 'Информация о компании обновлена'

#     def get_context_data(self, **kwargs):
#         company = Company.objects.get(owner_id=self.request.user.id)
#         form = CompanyForm(instance=company)
#         context = super(MyCompanyView, self).get_context_data(**kwargs)
#         context['company_edit'] = company
#         context['form'] = form
#         return context

#     def post(self, request, *args, **kwargs):
#         instance = Company.objects.get(owner_id=self.request.user.id)
#         form = CompanyForm(request.POST, request.FILES, instance=instance)
#         if form.is_valid():
#             print('valid')
#             form.save()
#             return redirect('my_company')
#         return render(request, 'accounts/company-edit.html', context={'form': form})


class MyCompanyVacanciesView(LoginRequiredMixin, CompanyAccessMixin, ListView):
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


class MyCompanyVacansyView(LoginRequiredMixin, CompanyAccessMixin, DetailView):
    template_name = 'accounts/vacancy-edit.html'
    model = Vacancy
    pk_url_kwarg = 'vacancy_id'

    def get_context_data(self, **kwargs):
        #vacancy = Vacancy.objects.get(id=self.kwargs['vacancy_id'])
        form_context = {
            'title': self.object.title,
            'specialty': self.object.specialty,
            'skills': self.object.skills,
            'description': self.object.description,
            'salary_min': self.object.salary_min,
            'salary_max': self.object.salary_max,
        }
        form = VacancyForm(form_context)
        context = super(MyCompanyVacansyView, self).get_context_data(**kwargs)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        instance = self.get_object(self.queryset)
        form = VacancyForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('my_company_vacancy', self.kwargs["vacancy_id"])
        return render(request, 'accounts/company-edit.html', context={'form': form})

# Create your views here.
