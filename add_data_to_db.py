import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
django.setup()

from data import jobs, companies, specialties
from app_jobsearch.models import Company, Specialty, Vacancy


if __name__ == '__main__':
    # Wipe all data from DB
    Company.objects.all().delete()
    Specialty.objects.all().delete()
    Vacancy.objects.all().delete()

    # Fill up DB with initial data
    for company in companies:
        Company.objects.create(name=company['title'], logo='https://place-hold.it/100x60',
                               location='Москва или удаленно')

    for specialty in specialties:
        Specialty.objects.create(code=specialty['code'],
                                 title=specialty['title'],
                                 picture='https://place-hold.it/100x60')

    for job in jobs:
        company = Company.objects.get(name=job['company'])
        specialty = Specialty.objects.get(code=job['cat'])
        Vacancy.objects.create(title=job['title'], specialty=specialty, company=company,
                               description=job['desc'], salary_min=job['salary_from'],
                               salary_max=job['salary_to'], published_at=job['posted'],
                               skills='Бэкенд, Средний (Middle), Python, PostgreSQL, MySQL')
