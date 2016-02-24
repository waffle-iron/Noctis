from django.shortcuts import render
from django.http import HttpResponse

from .models import nProject

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
    """
    Just a simple return of all projects in the database
    """
    projects = nProject.objects.order_by("-name")
    response_setup = "<html><body>Projects:<br/><ul>"
    end = "</ul></body></html>"
    for aProject in projects:
        response_setup += "<li>%s</li>"%aProject # returns str of name by default
    response_setup += end
    #print(get_client_ip(request))
    return HttpResponse(response_setup)