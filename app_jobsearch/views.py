from django.db.models import Count
from django.http import Http404, HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render
from django.views import View

from app_jobsearch.models import Company, Specialty, Vacancy


class MainView(View):
    def get(self, request):
        all_specialties = Specialty.objects.annotate(count=Count('vacancies'))
        all_companies = Company.objects.annotate(count=Count('vacancies'))
        context = {
            'specialties': all_specialties,
            'companies': all_companies
        }
        return render(request, 'app_jobsearch/index.html', context=context)


class AllVacanciesView(View):
    def get(self, request):
        all_vacancies = Vacancy.objects.order_by('-published_at')

        context = {
            'page_title': 'Все вакансии',
            'vacancies': all_vacancies,
            'number_of_vacancies': len(all_vacancies)
        }
        return render(request, 'app_jobsearch/vacancies.html', context=context)


class VacanciesBySpecialtyView(View):
    def get(self, request, specialty):
        # get an object for desired specialty from DB or None
        specialty_obj = Specialty.objects.filter(code=specialty).first()
        if specialty_obj is None:
            raise Http404

        vacancies_by_specialty = Vacancy.objects.filter(specialty=specialty_obj).order_by('-published_at')

        context = {
            'page_title': specialty_obj.title,
            'vacancies': vacancies_by_specialty,
            'number_of_vacancies': len(vacancies_by_specialty)
        }
        return render(request, 'app_jobsearch/vacancies.html', context=context)


class CompanyView(View):
    def get(self, request, company_id):
        company = Company.objects.filter(id=company_id).first()
        if company is None:
            raise Http404

        company_vacancies = Vacancy.objects.filter(company=company_id).order_by('-published_at')

        context = {
            'company': company,
            'vacancies': company_vacancies,
            'number_of_vacancies': len(company_vacancies)
        }
        return render(request, 'app_jobsearch/company.html', context=context)


class VacancyView(View):
    def get(self, request, vacancy_id):
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        if vacancy is None:
            raise Http404

        context = {
            'vacancy': vacancy
        }
        return render(request, 'app_jobsearch/vacancy.html', context=context)



def custom_handler404(request, exception):
    return HttpResponseNotFound('Кажется такой страницы не существует. Проверьте адрес!')


def custom_handler500(request):
    return HttpResponseServerError('Ой, что то сломалось... Простите, извините!')
