from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from django.http import Http404, HttpResponse, HttpRequest

def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')

@csrf_exempt
def process(request: HttpRequest) -> HttpResponse:
    print(request.body)
    return HttpResponse('success')