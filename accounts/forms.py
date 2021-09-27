from django import forms

from hiring.models import Company, Vacancy


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('name', 'logo', 'employee_count', 'location', 'description')
        labels = {
            'name': 'Название компании',
            'logo': 'Логотип',
            'employee_count': 'Количество человек в компании',
            'location': 'География',
            'description': 'Информация о компании',
        }


class VacancyForm(forms.ModelForm):

    class Meta:
        model = Vacancy
        fields = (
            'title',
            'specialty',
            'skills',
            'description',
            'salary_min',
            'salary_max',
        )
        labels = {
            'title': 'Название вакансии',
            'specialty': 'Специализация',
            'skills': 'Требуемые навыки',
            'description': 'Описание вакансии',
            'salary_min': 'Зарплата от',
            'salary_max': 'Зарплата до',
        }
