"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from app_jobsearch.views import MainView, AllVacanciesView, VacanciesBySpecialtyView, CompanyView, VacancyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main-view'),
    path('vacancies/', AllVacanciesView.as_view(), name='vacancies-view'),
    path('vacancies/cat/<str:specialty>/', VacanciesBySpecialtyView.as_view(), name='vacancies-by-specialty'),
    path('companies/<int:company_id>', CompanyView.as_view(), name='company-view'),
    path('vacancies/<int:vacancy_id>', VacancyView.as_view(), name='vacancy-view'),
]
