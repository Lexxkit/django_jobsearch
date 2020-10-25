from datetime import date

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import Http404, HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView

from .forms import RegistrationForm, ApplicationForm, CompanyForm, VacancyForm
from app_jobsearch.models import Company, Specialty, Vacancy, Application


class MainView(View):
    def get(self, request):
        all_specialties = Specialty.objects.annotate(vacancies_count=Count('vacancies'))
        all_companies = Company.objects.annotate(vacancies_count=Count('vacancies'))
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
            'vacancies': all_vacancies
        }
        return render(request, 'app_jobsearch/vacancies.html', context=context)


class VacanciesBySpecialtyView(View):
    def get(self, request, specialty):
        # get an object for desired specialty from DB or None
        specialty_obj = get_object_or_404(Specialty, code=specialty)

        vacancies_by_specialty = Vacancy.objects.filter(specialty=specialty_obj).order_by('-published_at')

        context = {
            'page_title': specialty_obj.title,
            'vacancies': vacancies_by_specialty
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
            'vacancies': company_vacancies
        }
        return render(request, 'app_jobsearch/company.html', context=context)


class VacancyView(View):
    def get(self, request, vacancy_id):
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)

        context = {
            'vacancy': vacancy,
            'form': ApplicationForm()
        }
        return render(request, 'app_jobsearch/vacancy.html', context=context)


class ApplicationView(View):
    def post(self, request, vacancy_id):
        form = ApplicationForm(request.POST)
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        if form.is_valid():
            application_data = form.cleaned_data
            application_data['user'] = request.user
            application_data['vacancy'] = vacancy
            Application.objects.create(**application_data)
            context = {
                'vacancy': vacancy,
            }
        return render(request, 'app_jobsearch/sent.html', context=context)


class MyCompanyView(View):
    def get(self, request):
        user_company = Company.objects.filter(owner=request.user.id).values().first()
        if user_company is None:
            # create mock-data to redirect user on 'company-edit' page
            Company.objects.create(name='Company', location='', logo='',
                                   description='', employee_count=0,
                                   owner=request.user)
            return render(request, 'app_jobsearch/company-create.html')

        form = CompanyForm(initial=user_company)
        context = {
            'company': user_company,
            'form': form
        }
        return render(request, 'app_jobsearch/company-edit.html', context=context)

    def post(self, request):
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            user_company = Company.objects.filter(owner=request.user.id).first()
            company_data = form.cleaned_data
            user_company.owner = request.user
            user_company.name = company_data['name']
            user_company.location = company_data['location']
            user_company.logo = company_data['logo']
            user_company.description = company_data['description']
            user_company.employee_count = company_data['employee_count']
            user_company.save()
            messages.success(request, 'Информация о компании обновлена')
            return redirect('user-company')

        user_company = Company.objects.filter(owner=request.user.id).values().first()
        context = {
            'company': user_company,
            'form': form
        }
        return render(request, 'app_jobsearch/company-edit.html', context=context)


class MyVacanciesAllView(View):
    def get(self, request):
        user_vacancies = Vacancy.objects.filter(company__owner=request.user) \
            .annotate(applications_count=Count('applications'))
        context = {
            'vacancies': user_vacancies
        }
        return render(request, 'app_jobsearch/vacancy-list.html', context=context)


class MyVacancyOneView(View):
    def get(self, request, vacancy_id):
        user_vacancy = Vacancy.objects.filter(id=vacancy_id).values().first()
        user_company = get_object_or_404(Company, owner=request.user.id)
        if user_vacancy is None:
            user_vacancy = Vacancy.objects.create(title='новая вакансия',
                                                  specialty=Specialty.objects.get(title='Фронтенд'),
                                                  company=user_company,
                                                  skills='навык',
                                                  description='',
                                                  salary_min=0,
                                                  salary_max=0,
                                                  published_at=date.today())
            user_vacancy = Vacancy.objects.filter(id=user_vacancy.id).values().first()

        form = VacancyForm(initial=user_vacancy)
        vacancy_applications = Application.objects.filter(vacancy=vacancy_id)
        context = {
            'form': form,
            'company': user_company,
            'vacancy': user_vacancy,
            'applications': vacancy_applications
        }
        return render(request, 'app_jobsearch/vacancy-edit.html', context=context)

    def post(self, request, vacancy_id):
        form = VacancyForm(request.POST)
        if form.is_valid():
            user_vacancy = Vacancy.objects.filter(id=vacancy_id).first()
            vacancy_data = form.cleaned_data
            user_vacancy.title = vacancy_data['title']
            user_vacancy.specialty = vacancy_data['specialty']
            user_vacancy.company = Company.objects.get(owner_id=request.user.id)
            user_vacancy.skills = vacancy_data['skills']
            user_vacancy.description = vacancy_data['description']
            user_vacancy.salary_min = vacancy_data['salary_min']
            user_vacancy.salary_max = vacancy_data['salary_max']
            user_vacancy.published_at = date.today()
            user_vacancy.save()
            messages.success(request, 'Вакансия обновлена')
            return redirect(reverse('user-vacancy', args=[vacancy_id]))
        return render(request, 'app_jobsearch/vacancy-edit.html', {'form': form})


class MyRegisterView(CreateView):
    form_class = RegistrationForm
    success_url = '/login'
    template_name = 'app_jobsearch/register.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'app_jobsearch/login.html'


def custom_handler404(request, exception):
    return HttpResponseNotFound('Кажется такой страницы не существует. Проверьте адрес!')


def custom_handler500(request):
    return HttpResponseServerError('Ой, что то сломалось... Простите, извините!')
