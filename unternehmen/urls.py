from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('branchen/', views.branchen, name='branchen'),
    path('unternehmensgroesse/', views.unternehmensgroesse, name='unternehmensgroesse'),
    path('boersennotierung/', views.boersennotierung ,name='boersennotierung'),
    path('daten/', views.daten, name='daten'),
    path('ueberuns/', views.ueberuns, name='ueberuns'),
    path('zusammenfassung/', views.zusammenfassung, name='zusammenfassung'),

]
