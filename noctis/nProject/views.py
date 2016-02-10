from django.shortcuts import render
from django.http import HttpResponse

from .models import nProject

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
	return HttpResponse(response_setup)