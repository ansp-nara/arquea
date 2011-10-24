# Create your views here.
from django.http import HttpResponse

def verifica(request):
    return HttpResponse('Ok')
