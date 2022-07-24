from django.shortcuts import render
from django.views import generic

from django.http import Http404, HttpResponse, HttpRequest

def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')