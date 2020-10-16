from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=32)
    logo = models.TextField()
    description = models.TextField()
    employee_count = models.IntegerField(default=0)


class Specialty(models.Model):
    code = models.CharField(max_length=32)
    title = models.CharField(max_length=128)
    picture = models.TextField()


class Vacancy(models.Model):
    title = models.CharField(max_length=128)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()
