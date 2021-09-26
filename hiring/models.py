from django.db import models
from django.contrib.auth.models import User
from djumanji_hiring.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Company(models.Model):
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, height_field='height_field', width_field='width_field')
    height_field = models.PositiveIntegerField(default=0)
    width_field = models.PositiveIntegerField(default=0)
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Company {self.name} from {self.location}'


class Specialty(models.Model):
    code = models.CharField(max_length=24)
    title = models.CharField(max_length=64)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR, height_field='height_field', width_field='width_field')
    height_field = models.PositiveIntegerField(default=0)
    width_field = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Specialty {self.title}'


class Vacancy(models.Model):
    title = models.CharField(max_length=124)
    specialty = models.ForeignKey(Specialty, related_name='vacancies', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='vacancies', on_delete=models.CASCADE)
    skills = models.CharField(max_length=200)
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_as = models.DateField()

    def __str__(self):
        return f'Vacancy {self.title}'


class Application(models.Model):
    written_username = models.CharField(max_length=124)
    written_phone = models.CharField(max_length=12)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, related_name='applications', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE)

    def __str__(self):
        return f'Application from {self.written_username}'


# Create your models here.
