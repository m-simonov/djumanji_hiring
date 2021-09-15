from django.core.management import BaseCommand

from hiring.models import Company, Specialty, Vacancy
import data as mock


class Command(BaseCommand):

    def handle(self, *args, **options):

        for company in mock.companies:
            Company.objects.create(
                name=company["title"],
                location=company["location"],
                description=company["description"],
                employee_count=company["employee_count"],
            )

        for specialty in mock.specialties:
            Specialty.objects.create(
                code=specialty["code"],
                title=specialty["title"],
            )

        for job in mock.jobs:
            Vacancy.objects.create(
                title=job["title"],
                specialty=Specialty.objects.get(code=job["specialty"]),
                company=Company.objects.get(id=job["company"]),
                skills=job["skills"],
                description=job["description"],
                salary_min=job["salary_from"],
                salary_max=job["salary_to"],
                published_as=job["posted"],
            )
