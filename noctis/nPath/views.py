from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("PATHING SETUP FOR NOCTIS: (Documentation to come...)")

def extract_basic(path):
    '''
    Simple initial data analysis on a path.
    '''
    out_ = {}
    path = path.replace("\\", "/")
    path_breakdown = path.split("/")
    out_['ext'] = path_breakdown[-1].split(".")[-1]
    out_['filename'] = ".".join(path_breakdown[-1].split(".")[:-1])
    
    ## Make sure we have an extension.
    if out_['ext'] == out_['filename']:
        return None

    out_['directory'] = "/".join(path_breakdown[:-1])
    return out_