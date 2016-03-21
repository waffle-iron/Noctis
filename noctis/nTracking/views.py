import sys
from django.shortcuts import render
from jsonrpc import jsonrpc_method

## Models:
from .models import nApprovalLevel
from .models import nStatusComponentLevel
from .models import nMainApproval

# Other Models:
from nAsset.models import nAsset
from nProject.models import nProject
from nProject.models import nProjectHub
from nProject.models import nProjectPart

'''
Methods
'''
def construct(self, class_name, **kwargs):
    tartget_class = getattr(sys.modules[__name__], class_name)
    return tartget_class.objects.get(**kwargs)

'''
Status
'''
@jsonrpc_method('nTracking.get_all_status_component_levels() -> list')
def get_all_status_component_levels(request):
    """
    Simple RPC to call all CL names in the database.
    """
    _status_components = nStatusComponentLevel.objects.all()
    return [i.name for i in _status_components]

'''
Approvals
'''
@jsonrpc_method("nTracking.add_approval_level(str) -> bool")
def add_approval_level(request, level_name=""):
    """
    Add an nApprovalLevel.
    """
    _new_approval = nApprovalLevel(name=level_name)
    _new_approval.save()
    return _new_approval

@jsonrpc_method("nTracking.make_approval(dict) -> dict")
def make_approval(request, approal_info={}):
    """
    For a nMainApproval. This can be a intense transaction but
    will give us plenty of control when it comes to creating/modifying
    an approval.
    
    @param::approal_info: The dictionary with all optional (at least 2)
    pointers needed.
    @type::approal_info: D{ pointer_type(str) : pointer_id(int) }
    """
    info_keys = [ "asset_pointer", "project_pointer", "hub_pointer", "part_pointer" ]
    info_to_name = { "asset_pointer"   : "nAsset",
                     "project_pointer" : "nProject",
                     "hub_pointer"     : "nProjectHub",
                     "part_pointer"    : "nProjectPart" }

    if len(approal_info.keys()) < 2:
        return { "error" : "info dict doesn't have enough keys." }

    _data = {}
    for a_key in approal_info.keys():
        if a_key not in info_keys:
            return { "error" : "%s not a proper pointer key"%a_key }
        _data[a_key] = construct(approal_info[a_key], info_to_name[a_key])

    the_approval = nMainApproval(**_data)
    the_approval.save()

    return nMainApproval.to_dict([the_approval])[0]