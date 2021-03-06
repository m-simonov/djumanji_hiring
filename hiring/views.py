from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, TemplateView

from hiring.forms import ApplicationForm
from hiring.models import Company, Specialty, Vacancy


class MainView(TemplateView):
    template_name = 'hiring/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(vacancy_count=Count('vacancies'))
        context['companies'] = Company.objects.annotate(vacancy_count=Count('vacancies'))
        return context


class VacanciesView(ListView):
    template_name = 'hiring/vacancies.html'
    model = Vacancy
    context_object_name = 'vacancies'

    def get_context_data(self, **kwargs):
        context = super(VacanciesView, self).get_context_data(**kwargs)
        context['title'] = "Все вакансии"
        return context


class VacanciesCategoryView(ListView):
    template_name = 'hiring/vacancies.html'
    model = Vacancy
    context_object_name = 'vacancies'
    pk_url_kwarg = 'category'

    def get_queryset(self):
        self.specialty = get_object_or_404(Specialty, code=self.kwargs['category'])
        return Vacancy.objects.filter(specialty=self.specialty)

    def get_context_data(self, **kwargs):
        context = super(VacanciesCategoryView, self).get_context_data(**kwargs)
        context['title'] = self.specialty.title
        return context


class CompanyView(DetailView):
    template_name = 'hiring/company.html'
    model = Company
    context_object_name = 'company'
    pk_url_kwarg = 'company_id'

    def get_context_data(self, **kwargs):
        context = super(CompanyView, self).get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.filter(company=self.kwargs['company_id'])
        return context


class VacancyView(DetailView):
    template_name = 'hiring/vacancy.html'
    model = Vacancy
    context_object_name = 'vacancy'
    pk_url_kwarg = 'vacancy_id'

    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        context['company_name'] = self.object.company.name
        context['employee_count'] = self.object.company.employee_count
        context['location'] = self.object.company.location
        context['form'] = ApplicationForm
        return context

    def post(self, request, *args, **kwargs):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            form.instance.vacancy_id = self.kwargs['vacancy_id']
            form.instance.user_id = request.user.id
            application.save()
            return redirect('sent', self.kwargs['vacancy_id'])
        return render(request, 'hiring/vacancy.html', context={'form': form})


def custom_handler_404(request, exception):
    return HttpResponseNotFound('Неверный запрос')


def custom_handler_500(request):
    return HttpResponseServerError('Ошибка сервера')

# Create your views here.
