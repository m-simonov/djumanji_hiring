from django.contrib import admin

from .models import Application, Company, Specialty, Vacancy


class CompanyAdmin(admin.ModelAdmin):
    pass


class SpecialtyAdmin(admin.ModelAdmin):
    pass


class VacancyAdmin(admin.ModelAdmin):
    pass


class ApplicationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company, CompanyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Application, ApplicationAdmin)

# Register your models here.
