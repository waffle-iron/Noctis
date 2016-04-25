from django.shortcuts import render
from jsonrpc import jsonrpc_method

## User Authentication.
from django.contrib.auth.decorators import permission_required

## Other models:
from nPath.models import nPath
from nPath.views import extract_basic
from nProject.models import nProjectPart
from nProject.models import nProjectHub

## Models:
from .models import nAsset
from .models import nAssetType
from .models import nVersionController

## Other/Misc:
from noctis import utils

@jsonrpc_method("nAsset.create_asset(str, str, int, str, str, str) -> dict",
                authenticated=True)
def create_asset(request, asset_pointer="", asset_type="", version=0,
                 asset_name="", hub_name="", project_name=""):  
    """
    Create an nAsset. This takes quite a few params but needs to be potent and
    well connected. This has to point quite a few directions without being dependent
    on too much.

    @params
    $asset_pointer : (str) : give us the path we;re working with.

    $asset_type : (str) : What kind of asset is this?

    $version : (int) : The version of the asset we're going to add

    $asset_name : (str) : Name to be tied to the asset for Version Group control

    $hub_name : (str) : The name associated with this

    $return : (dict) : New asset in dict form.
    """
    if request:
        _u = utils.get_username(request)
    else:
        _u = "aimee"
    _a_type = nAssetType.objects.get(name=asset_type)

    ## Pathing break down to give us any other information we'll
    ## need. This gives us fine tuned control as long as the path
    ## minimums are kept in the setup.
    _path_data = extract_basic(asset_pointer)
    if not _path_data:
        e = "The path: %s isn't compatible with Nocits."%asset_pointer
        e += "(There must be an extension)"
        raise TypeError(e)
    # path_setup = nPath.objects.get(extension=_path_data['ext'], asset_type=asset_type)
    hub = nProjectHub.objects.get(name=hub_name, project__name=project_name)

    ## Getting the version controller requires knowing the project name
    version_control, created = nVersionController.objects.get_or_create(hub_pointer=hub,
                                                                       group_name=asset_name,
                                                                       asset_type=_a_type)

    if version_control.highest_version < version:
        version_control.highest_version = version
        version_control.save() # To keep our new data

    asset = nAsset.objects.create(asset_pointer=asset_pointer,
                                  version=version,
                                  version_controller=version_control,
                                  author=_u)

    return nAsset.make_dicts(nAsset.objects.filter(id=asset.id))[0]

@jsonrpc_method("nAsset.get_asset_from_pointer(str) -> dict",
                authenticated=True)
def get_asset_from_pointer(request, pointer=""):
    '''
    Retrieve an asset from its pointer. It's unique so therefore
    can be found.

    @params
    $pointer : (str) : pointer value of the asset we want. (Unique)

    $return : (dict) : Full asset information.
    '''
    asset_filter = nAsset.objects.filter(asset_pointer=pointer)

    if asset_filter.exists():
        return nAsset.make_dicts(asset_filter)[0]
    else:
        return {}

@jsonrpc_method("nAsset.get_assets_from_pointer_list(list) -> list",
                authenticated=True)
def get_assets_from_pointer_list(request, list_of_pointers=[]):
    '''
    Retrieve multiple assets from a list of pointers.

    @params
    $list_of_pointers : (list) : All pointers we want to use.

    $return : (list) : List of assets in dict form
    '''
    asset_filter = nAsset.objects.filter(asset_pointer__in=list_of_pointers)

    if asset_filter.exists():
        return nASset.make_dicts(asset_filter)
    else:
        return []

@jsonrpc_method("nAsset.version_up_asset(int, str, bool) -> bool",
                authenticated=True)
def version_up_asset(request, asset_id=0, asset_pointer=""):
    '''
    Since version handling is done via django we can pass to and
    update the proper controllers.

    NOTE: This will eventually be completely django handled once
    the nPath app is more built-in.

    @params
    $asset_id : (int) : ID of the asset we're version-ing off of in our
    database.

    $asset_pointer : (str) : Pointer to the asset we'll be creating.

    $return : (bool) : If the version up was successful. 
    '''
    _u = utils.get_username(request)
    current_asset = nAsset.objects.get(id=asset_id)
    vc = current_asset.version_controller

    new_asset = nAsset.objects.create(asset_pointer=asset_pointer,
                                      version=(vc.highest_version + 1),
                                      version_controller=vc,
                                      author=_u)

    vc.versionUp()
    vc.save()

    return True
    ## TODO: Check and finish
