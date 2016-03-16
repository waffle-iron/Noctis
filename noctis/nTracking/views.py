from django.shortcuts import render
from jsonrpc import jsonrpc_method

## Models:
from .models import nStatusComponentLevel

@jsonrpc_method('nTracking.get_all_status_component_levels() -> list')
def get_all_status_component_levels(request):
    """
    Simple RPC to call all CL names in the database.
    """
    _status_components = nStatusComponentLevel.objects.all()
    return [i.name for i in _status_components]