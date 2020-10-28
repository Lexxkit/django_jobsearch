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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from app_jobsearch.views import MainView, AllVacanciesView, VacanciesBySpecialtyView, CompanyView, VacancyView, \
    ApplicationView, MyCompanyView, MyVacanciesAllView, MyVacancyOneView, custom_handler404, custom_handler500, \
    MyLoginView, MyRegisterView, create_mycompany, create_myresume, MyResumeView, MySearchView

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main'),
    path('vacancies/', AllVacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:specialty>/', VacanciesBySpecialtyView.as_view(), name='vacancies-by-specialty'),
    path('companies/<int:company_id>', CompanyView.as_view(), name='company'),
    path('vacancies/<int:vacancy_id>', VacancyView.as_view(), name='vacancy'),
    path('vacancies/<int:vacancy_id>/send', ApplicationView.as_view(), name='sent'),
    path('mycompany/', MyCompanyView.as_view(), name='user-company'),
    path('mycompany/create/', create_mycompany, name='create-mycompany'),
    path('mycompany/vacancies/', MyVacanciesAllView.as_view(), name='user-vacancies'),
    path('mycompany/vacancies/<int:vacancy_id>', MyVacancyOneView.as_view(), name='user-vacancy'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', MyRegisterView.as_view(), name='register'),
    path('myresume/create', create_myresume, name='create-myresume'),
    path('myresume/', MyResumeView.as_view(), name='user-resume'),
    path('search/', MySearchView.as_view(), name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
