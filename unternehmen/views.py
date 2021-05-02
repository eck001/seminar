from django.shortcuts import render
from django.http import HttpResponse
from unternehmen.models import *

# Create your views here.
def home(request):
    return render(request, 'base.html')

def unternehmen(request):
    details_for_front_end = details.objects.filter(unternehmensname="Yahoo")

    return render(request, 'Unternehmen/yahoo.html', {'details' : details_for_front_end})

def branchen(request):
    return  render(request, 'Seiten/branchen.html')
def unternehmensgroesse(request):
    return  render(request, 'Seiten/unternehmensgrosse.html')

def boersennotierung(request):
    return  render(request, 'Seiten/boersennotierung.html')

def daten(request):
    return  render(request, 'Seiten/daten.html')

def ueberuns(request):
    return  render(request, 'Seiten/ueberuns.html')