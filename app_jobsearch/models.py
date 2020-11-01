from django.contrib.auth import get_user_model
from django.db import models

from conf.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR
from data import WorkStatusChoices, GradeChoices, EducationChoices


class Company(models.Model):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=32)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, null=True)
    description = models.TextField()
    employee_count = models.IntegerField(default=0)
    owner = models.OneToOneField(get_user_model(),
                                 on_delete=models.CASCADE,
                                 related_name='mycompany')


class Specialty(models.Model):
    code = models.CharField(max_length=32)
    title = models.CharField(max_length=128)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    title = models.CharField(max_length=128)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()


class Application(models.Model):
    written_username = models.CharField(max_length=128)
    written_phone = models.CharField(max_length=32)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='applications')


class Resume(models.Model):
    user = models.OneToOneField(get_user_model(),
                                on_delete=models.CASCADE,
                                related_name='resume')
    name = models.CharField(max_length=25, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    status = models.CharField(max_length=32, choices=WorkStatusChoices.choices(),
                              verbose_name='Готовность к работе')
    salary = models.IntegerField(verbose_name='Ожидаемое вознаграждение')
    specialty = models.ForeignKey(Specialty, on_delete=models.PROTECT, related_name='resume',
                                  verbose_name='Специализация')
    grade = models.CharField(max_length=32, choices=GradeChoices.choices(),
                             verbose_name='Квалификация')
    education = models.CharField(max_length=32, choices=EducationChoices.choices(),
                                 verbose_name='Уровень образования')
    education_name = models.TextField(null=True, blank=True,
                                      verbose_name='Наименование учебной организации')
    experience = models.TextField(null=True, blank=True,
                                  verbose_name='Опыт работы')
    portfolio = models.URLField(null=True, blank=True,
                                verbose_name='Ссылка на портфолио')
