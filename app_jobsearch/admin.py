from django.contrib import admin

from .models import Company, Specialty, Vacancy, Application


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'location',
        'logo',
        'description',
        'employee_count',
        'owner',
    )
    list_filter = ('owner',)
    search_fields = ('name',)


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'title', 'picture')


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'specialty',
        'company',
        'skills',
        'description',
        'salary_min',
        'salary_max',
        'published_at',
    )
    list_filter = ('specialty', 'company', 'published_at')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'written_username',
        'written_phone',
        'written_cover_letter',
        'vacancy',
        'user',
    )
    list_filter = ('vacancy', 'user')
