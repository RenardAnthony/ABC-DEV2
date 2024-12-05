from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings



# Create your views here.
def regles_general(request):
    return render(request, 'regles/regles_general.html')