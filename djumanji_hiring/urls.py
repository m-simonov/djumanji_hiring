"""djumanji_hiring URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from accounts.views import (CreateMyCompanyView, CreateVacancyView,
                            LetsStartMyCompanyView, MyCompanyVacanciesView,
                            MyCompanyVacancyView, MyCompanyView, MyLoginView,
                            MySignupView, SentView)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from hiring.views import (CompanyView, MainView, VacanciesCategoryView,
                          VacanciesView, VacancyView, custom_handler_404,
                          custom_handler_500)

handler404 = custom_handler_404
handler500 = custom_handler_500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:category>', VacanciesCategoryView.as_view(), name='category'),
    path('companies/<int:company_id>', CompanyView.as_view(), name='company'),
    path('vacancies/<int:vacancy_id>', VacancyView.as_view(), name='vacancy'),

    path('vacancies/<int:vacancy_id>/send/', SentView.as_view(), name='sent'),
    path('mycompany/letsstart/', LetsStartMyCompanyView.as_view(), name='letsstart'),
    path('mycompany/create/', CreateMyCompanyView.as_view(), name='create_my_company'),
    path('mycompany/', MyCompanyView.as_view(), name='my_company'),
    path('mycompany/vacancies/', MyCompanyVacanciesView.as_view(), name='my_company_vacancies'),
    path('mycompany/vacancies/create/', CreateVacancyView.as_view(), name='create_vacancy'),
    path('mycompany/vacancies/<int:vacancy_id>', MyCompanyVacancyView.as_view(), name='my_company_vacancy'),
]

urlpatterns += [
    path('login/', MyLoginView.as_view(), name='login'),
    path('signup/', MySignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
